from src.feature_extractor import extract_features

def test_extract_features_basic():
    text = "This is a short test."
    f = extract_features(text)
    assert isinstance(f['word_count'], int)
    assert f['word_count'] > 0
