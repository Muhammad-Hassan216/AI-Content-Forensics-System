from src.feature_extractor import extract_features
from src.detector import detect
from src.classifier import predict_proba


text = (
    "In recent years, language models have advanced rapidly, producing coherent human-like prose across many domains."
)

f = extract_features(text)

def show(res):
    print('label:', res.get('label'))
    print('ensemble:', round(res.get('score', 0), 4))
    print('ml_prob:', round(res.get('ml_prob', 0), 4))
    print('heuristic_prob:', round(res.get('heuristic_prob', 0), 4))
    print('---')

print('Running default (threshold=0.5, ml_weight=0.5)')
res = detect(f, text=text, threshold=0.5, ml_weight=0.5)
show(res)

print('Increasing ml_weight -> 0.8')
res2 = detect(f, text=text, threshold=0.5, ml_weight=0.8)
show(res2)

print('Lower threshold -> 0.3 (ml_weight=0.5)')
res3 = detect(f, text=text, threshold=0.3, ml_weight=0.5)
show(res3)

print('Direct ML model probability via classifier.predict_proba:')
try:
    ml = predict_proba(text)
    print('predict_proba:', round(ml, 4))
except Exception as e:
    print('predict_proba failed:', e)
