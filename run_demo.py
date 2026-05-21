import json
from src.feature_extractor import extract_features
from src.detector import detect
from src.explainer import explain
from src import classifier

sample_texts = {
    "Human-like": "I wrote this after checking the source twice and then compared the results with the original note.",
    "AI-like": "This comprehensive analysis highlights the multifaceted implications of the proposed framework in a concise and structured manner.",
    "Long AI-like (demo)": (
        "In recent years, rapid advancements in generative models have produced highly coherent "
        "and contextually relevant text. This example demonstrates verbosity, formal phrasing, "
        "and low punctuation density commonly found in model-generated outputs."
    ),
}

results = {}
for name, text in sample_texts.items():
    features = extract_features(text)
    detection = detect(features, text=text, threshold=0.5)
    explanation = explain(features, detection)
    # optional ML model probability
    mdl = classifier.load_model()
    ml_prob = None
    if mdl is not None:
        try:
            ml_prob = classifier.predict_proba(text, model=mdl)
        except Exception:
            ml_prob = None
    results[name] = {
        'text': text,
        'features': features,
        'detection': detection,
        'explanation': explanation,
        'ml_prob': ml_prob,
    }

print("Demo results:\n")
for name, r in results.items():
    print(f"== {name} ==")
    print(f"Label: {r['detection']['label']}, Score: {r['detection']['score']:.3f}")
    if r['detection'].get('ml_prob') is not None:
        print(f"ML model AI prob: {r['detection']['ml_prob']:.3f}")
    print(f"Heuristic prob: {r['detection'].get('heuristic_prob'):.3f}")
    print(f"Word count: {r['features']['word_count']}")
    print("Contributions:")
    for k, v in r['explanation']['contributions'].items():
        print(f"  - {k}: raw={v['raw']}, pct={v['percent']}%")
    print()

with open('demo_output.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved detailed JSON output to demo_output.json")
