import re
from collections import Counter

def highlight_tokens(text, top_n=30):
    """Return HTML with tokens highlighted by simple heuristics:
    - repeated words: red background
    - long words (len>7): orange background
    - stopwords: dimmed color
    This is a lightweight alternative to SHAP for demo explainability.
    """
    if not text:
        return ""

    # split into words and non-word tokens
    words = re.findall(r"\w+|[^\w\s]", text)
    lowered = [w.lower() for w in words]
    counts = Counter([w for w in lowered if re.match(r"\w+", w)])
    stopwords = set(["the","and","is","in","to","of","a","with","for","on","this","that","it","as","are"])

    out = []
    for w in words:
        key = w.lower()
        style = ''
        title = ''
        if re.match(r"\w+", w):
            if counts.get(key, 0) > 1:
                style = 'background:#ffd6d6;border-radius:2px;padding:2px'
                title = f'Repeated ({counts[key]}x)'
            elif len(w) > 7:
                style = 'background:#ffe8cc;border-radius:2px;padding:2px'
                title = 'Long word'
            elif key in stopwords:
                style = 'color:#777'
                title = 'Stopword'

        esc = (w.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
        if style:
            out.append(f"<span style=\"{style}\" title=\"{title}\">{esc}</span>")
        else:
            out.append(esc)

    return ' '.join(out)
