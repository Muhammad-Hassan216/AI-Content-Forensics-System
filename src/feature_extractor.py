import re
import math

STOPWORDS = set([
    "the","and","is","in","it","of","to","a","that","this","for","on","with","as","are"
])

def tokenize(text):
    words = re.findall(r"\w+", text.lower())
    return words

def avg_word_length(words):
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)

def type_token_ratio(words):
    if not words:
        return 0.0
    return len(set(words)) / len(words)

def punctuation_ratio(text):
    if not text:
        return 0.0
    punct = sum(1 for c in text if c in '.,;:!?')
    return punct / max(1, len(text))

def stopword_ratio(words):
    if not words:
        return 0.0
    s = sum(1 for w in words if w in STOPWORDS)
    return s / len(words)

def repeat_word_fraction(words):
    if not words:
        return 0.0
    from collections import Counter
    c = Counter(words)
    repeats = sum(1 for v in c.values() if v > 1)
    return repeats / len(c)

def extract_features(text):
    words = tokenize(text)
    features = {
        'avg_word_length': avg_word_length(words),
        'type_token_ratio': type_token_ratio(words),
        'punctuation_ratio': punctuation_ratio(text),
        'stopword_ratio': stopword_ratio(words),
        'repeat_word_fraction': repeat_word_fraction(words),
        'word_count': len(words)
    }
    # include raw text to support token-level explainability
    features['raw_text'] = text
    return features
