def explain(features, detection):
    """
    Provide a simple feature-contribution style explanation.
    """
    contributions = {}
    # mirror detector weights for explanation clarity
    base_weights = {
        'avg_word_length': 0.2,
        'type_token_ratio': -0.4,
        'punctuation_ratio': -0.2,
        'stopword_ratio': -0.1,
        'repeat_word_fraction': 0.5,
    }

    # compute raw contributions
    raw = {}
    for k, w in base_weights.items():
        v = features.get(k, 0)
        if k == 'avg_word_length':
            v = v / 6.0
        if k == 'punctuation_ratio':
            v = v * 10
        raw[k] = w * v

    # normalize to total explanatory magnitude and round for display
    total = sum(abs(v) for v in raw.values()) or 1.0
    for k, v in raw.items():
        contributions[k] = {'raw': round(v, 4), 'percent': round(100 * (abs(v) / total), 1)}

    explanation = {
        'label': detection.get('label'),
        'score': detection.get('score'),
        'contributions': contributions
    }

    # Add naive token-level contributions by mapping feature contributions to tokens
    try:
        token_contribs = {}
        text = features.get('raw_text', '') or ''
        if text:
            import re
            toks = re.findall(r"\w+", text)
            if toks:
                # feature raw values
                feat_raw = {k: v['raw'] for k, v in contributions.items()}
                from collections import Counter
                counts = Counter(toks)
                for t in set(toks):
                    score = 0.0
                    if len(t) > 7:
                        score += feat_raw.get('avg_word_length', 0) * (len(t) / 10.0)
                    if counts[t] > 1:
                        score += feat_raw.get('repeat_word_fraction', 0) * counts[t]
                    if t.lower() in ('the','and','is','in','to','of','a','with','for','on','this','that','it'):
                        score += feat_raw.get('stopword_ratio', 0)
                    token_contribs[t] = round(score, 4)
        explanation['token_contributions'] = dict(sorted(token_contribs.items(), key=lambda x: -abs(x[1]))[:40])
    except Exception:
        explanation['token_contributions'] = {}

    return explanation
