import os
import json
import re
from collections import defaultdict

MODEL_FILE = os.path.join(os.path.dirname(__file__), '..', 'models', 'simple_model.json')

def _tokenize(text):
    return re.findall(r"\w+", text.lower())

def train_and_save_simple_model(model_path=None):
    """Train a tiny Multinomial Naive Bayes on synthetic data and save to JSON.
    This implementation has no external dependencies.
    """
    # synthetic dataset (same intent as sklearn pipeline)
    human_texts = [
        "I checked the source and wrote this summary after careful review.",
        "Yesterday I visited the lab and took notes on the experiment results.",
        "The meeting concluded with specific action items assigned to each member.",
        "I prefer to write in a conversational tone with some informal expressions.",
        "This paragraph reflects my personal experience and opinions about the topic."
    ]
    ai_texts = [
        "This comprehensive analysis highlights the multifaceted implications of the proposed framework.",
        "The model generates coherent and contextually rich passages at scale with consistent style.",
        "This synthetic example demonstrates the verbose and formal phrasing common in generated text.",
        "The architecture produces text with low variability in lexical choice and high fluency.",
        "Automated generation often yields longer sentences with balanced structure and formal tone."
    ]

    class_counts = [defaultdict(int), defaultdict(int)]
    total_words = [0, 0]
    vocab = set()

    for t in human_texts:
        toks = _tokenize(t)
        for w in toks:
            class_counts[0][w] += 1
            total_words[0] += 1
            vocab.add(w)

    for t in ai_texts:
        toks = _tokenize(t)
        for w in toks:
            class_counts[1][w] += 1
            total_words[1] += 1
            vocab.add(w)

    model = {
        'vocab_size': len(vocab),
        'class_priors': [len(human_texts), len(ai_texts)],
        'total_words': total_words,
        'class_counts': { '0': dict(class_counts[0]), '1': dict(class_counts[1]) }
    }

    if model_path is None:
        model_path = os.path.abspath(MODEL_FILE)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'w', encoding='utf-8') as f:
        json.dump(model, f)
    return model_path


def train_from_dataset(texts, labels, model_path=None):
    """Train simple NB model from provided lists of texts and labels (0=human,1=ai)."""
    if len(texts) != len(labels):
        raise ValueError('texts and labels must match length')

    class_counts = [defaultdict(int), defaultdict(int)]
    total_words = [0, 0]
    vocab = set()

    for t, lab in zip(texts, labels):
        toks = _tokenize(t)
        c = 1 if int(lab) else 0
        for w in toks:
            class_counts[c][w] += 1
            total_words[c] += 1
            vocab.add(w)

    model = {
        'vocab_size': len(vocab),
        'class_priors': [0, 0],
        'total_words': total_words,
        'class_counts': { '0': dict(class_counts[0]), '1': dict(class_counts[1]) }
    }
    # simple priors from counts
    model['class_priors'][0] = sum(1 for l in labels if int(l) == 0)
    model['class_priors'][1] = sum(1 for l in labels if int(l) == 1)

    if model_path is None:
        model_path = os.path.abspath(MODEL_FILE)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'w', encoding='utf-8') as f:
        json.dump(model, f)
    return model_path

def load_simple_model(model_path=None):
    if model_path is None:
        model_path = os.path.abspath(MODEL_FILE)
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def predict_proba(texts, model=None):
    """Return probability of AI-generated for input texts (single str or list).
    Model should be the dict returned by load_simple_model.
    """
    single = False
    if isinstance(texts, str):
        texts = [texts]
        single = True
    if model is None:
        model = load_simple_model()
    if model is None:
        return None

    results = []
    vocab_size = model.get('vocab_size', 0)
    class_counts = {0: model['class_counts']['0'], 1: model['class_counts']['1']}
    total_words = model['total_words']
    priors = model['class_priors']

    for text in texts:
        toks = _tokenize(text)
        log_probs = [0.0, 0.0]
        for c in (0,1):
            # start with log prior (use counts)
            import math
            log_probs[c] = math.log(priors[c] / (priors[0] + priors[1]))
            for w in toks:
                count = class_counts[c].get(w, 0)
                # Laplace smoothing
                prob_w = (count + 1) / (total_words[c] + vocab_size + 1)
                log_probs[c] += math.log(prob_w)

        # normalize to probabilities
        import math
        maxlp = max(log_probs)
        exps = [math.exp(lp - maxlp) for lp in log_probs]
        s = sum(exps)
        probs = [e / s for e in exps]
        # class 1 is AI-generated
        results.append(probs[1])

    return results[0] if single else results
