from pathlib import Path


def detect(features, text=None, threshold=0.5, ml_weight=0.5):
    """
    Simple heuristic detector: compute a score from weighted features.
    Higher score means more likely AI-generated in this prototype.
    """
    # weights chosen for demonstration only
    weights = {
        'avg_word_length': 0.2,
        'type_token_ratio': -0.4,
        'punctuation_ratio': -0.2,
        'stopword_ratio': -0.1,
        'repeat_word_fraction': 0.5,
        'word_count': 0.0
    }

    # normalize some features roughly
    score = 0.0
    score += weights['avg_word_length'] * (features.get('avg_word_length', 0) / 6.0)
    score += weights['type_token_ratio'] * features.get('type_token_ratio', 0)
    score += weights['punctuation_ratio'] * (features.get('punctuation_ratio', 0) * 10)
    score += weights['stopword_ratio'] * features.get('stopword_ratio', 0)
    score += weights['repeat_word_fraction'] * features.get('repeat_word_fraction', 0)

    # map heuristic score to 0..1 via sigmoid (scaled)
    import math
    heuristic_prob = 1 / (1 + math.exp(-6 * (score - 0.0)))

    # try to use ML classifier if available and a saved model exists
    ml_prob = None
    try:
        if text is not None:
            from src.classifier import predict_proba, load_model
            mdl = load_model()
            if mdl is not None:
                p = predict_proba(text, model=mdl)
                if p is not None:
                    ml_prob = float(p)
    except Exception:
        ml_prob = None

    # simple ensemble: weighted average (ml_weight for ML, rest heuristic)
    final_prob = heuristic_prob
    if ml_prob is not None:
        try:
            w = float(ml_weight)
            w = max(0.0, min(1.0, w))
        except Exception:
            w = 0.5
        final_prob = (1.0 - w) * heuristic_prob + w * ml_prob

    label = 'AI-generated' if final_prob >= threshold else 'Human-written'
    return {'score': final_prob, 'label': label, 'heuristic_prob': heuristic_prob, 'ml_prob': ml_prob}
