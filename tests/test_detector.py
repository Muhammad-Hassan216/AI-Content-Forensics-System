from src.feature_extractor import extract_features
from src.detector import detect

def test_detect_returns_keys():
    text = "Simple sentence for testing detection."
    f = extract_features(text)
    d = detect(f, text=text)
    assert 'score' in d and 'label' in d
