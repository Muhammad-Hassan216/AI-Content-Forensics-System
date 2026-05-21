import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.joblib')

def is_sklearn_available():
    try:
        import sklearn
        return True
    except Exception:
        return False

def train_and_save_model(model_path=None):
    """Train a small TF-IDF + LogisticRegression model on lightweight synthetic examples and save it."""
    # If scikit-learn is available, train sklearn pipeline; otherwise use simple fallback
    if is_sklearn_available():
        from sklearn.pipeline import FeatureUnion, make_pipeline
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from joblib import dump
        import os

        # Small synthetic dataset — replace with real labeled data for production
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

        X = human_texts + ai_texts
        y = [0] * len(human_texts) + [1] * len(ai_texts)

        # Word + character features tend to improve robustness on short and stylistically varied text.
        features = FeatureUnion([
            ("word_tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=4000, lowercase=True)),
            ("char_tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000, lowercase=True)),
        ])
        pipeline = make_pipeline(
            features,
            LogisticRegression(max_iter=2000, class_weight='balanced')
        )
        pipeline.fit(X, y)

        if model_path is None:
            model_path = os.path.abspath(MODEL_PATH)

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        dump(pipeline, model_path)
        return model_path
    else:
        # fallback to simple pure-Python NB classifier
        try:
            from src.simple_classifier import train_and_save_simple_model
            return train_and_save_simple_model()
        except Exception:
            raise RuntimeError('Neither scikit-learn nor simple fallback available')

def load_model(model_path=None):
    import os
    # prefer sklearn joblib model if present
    if model_path is None:
        model_path = os.path.abspath(MODEL_PATH)
    if os.path.exists(model_path) and is_sklearn_available():
        from joblib import load
        return load(model_path)

    # try pure-python simple model
    try:
        from src.simple_classifier import load_simple_model
        simple = load_simple_model()
        if simple is not None:
            return simple
    except Exception:
        pass

    return None

def predict_proba(texts, model=None):
    """Return probability of AI-generated for input texts (single str or list)."""
    # If model is an sklearn pipeline, use its predict_proba
    if model is None:
        model = load_model()
    if model is None:
        return None

    # sklearn pipeline object has predict_proba
    if hasattr(model, 'predict_proba'):
        single = False
        if isinstance(texts, str):
            texts = [texts]
            single = True
        probs = model.predict_proba(texts)
        ai_probs = [float(p[1]) for p in probs]
        return ai_probs[0] if single else ai_probs

    # otherwise assume it's the simple model dict and use simple_classifier.predict_proba
    try:
        from src.simple_classifier import predict_proba as simple_predict
        return simple_predict(texts, model=model)
    except Exception:
        return None
