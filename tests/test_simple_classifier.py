from src.simple_classifier import train_from_dataset, load_simple_model, predict_proba

def test_simple_train_and_predict(tmp_path):
    texts = ["Hello world", "This is generated text likely AI"]
    labels = [0, 1]
    path = tmp_path / "model.json"
    model_path = train_from_dataset(texts, labels, model_path=str(path))
    assert model_path
    m = load_simple_model(model_path)
    assert m is not None
    p = predict_proba("Hello world", model=m)
    assert isinstance(p, float)
