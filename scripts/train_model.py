"""Train and save the small TF-IDF + LogisticRegression model.
Usage:
  python scripts/train_model.py
"""
import os
import sys
import csv
# ensure project root is on sys.path so `src` package is importable when running from scripts/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.classifier import train_and_save_model, is_sklearn_available


DEFAULT_LABELED_DATASET = os.path.join(ROOT, 'AI Generated Essays Dataset.csv')


def load_labeled_dataset(csv_path):
    texts = []
    labels = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = [name.strip().lstrip('\ufeff') for name in (reader.fieldnames or [])]
        if not fieldnames or 'text' not in fieldnames:
            raise RuntimeError('CSV must have a text column')

        label_column = None
        for candidate in ('label', 'generated'):
            if candidate in fieldnames:
                label_column = candidate
                break

        if label_column is None:
            raise RuntimeError('CSV must have a label or generated column')

        for row in reader:
            normalized_row = {
                (key or '').strip().lstrip('\ufeff'): value
                for key, value in row.items()
            }
            text = (normalized_row.get('text') or '').strip()
            label = (normalized_row.get(label_column) or '').strip()
            if text and label in {'0', '1'}:
                texts.append(text)
                labels.append(int(label))
    if not texts:
        raise RuntimeError(f'No valid labeled rows found in {csv_path}')
    return texts, labels


def calibrate_threshold(texts, labels):
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import FeatureUnion, make_pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import precision_recall_curve, precision_score, recall_score, f1_score, accuracy_score

    X_train, X_val, y_train, y_val = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    features = FeatureUnion([
        ("word_tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=4000, lowercase=True)),
        ("char_tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000, lowercase=True)),
    ])
    pipeline = make_pipeline(
        features,
        LogisticRegression(max_iter=2000, class_weight='balanced')
    )
    pipeline.fit(X_train, y_train)
    probs = [float(p[1]) for p in pipeline.predict_proba(X_val)]

    def heuristic_prob_from_text(text):
        import math
        from src.feature_extractor import extract_features

        features = extract_features(text)
        weights = {
            'avg_word_length': 0.2,
            'type_token_ratio': -0.4,
            'punctuation_ratio': -0.2,
            'stopword_ratio': -0.1,
            'repeat_word_fraction': 0.5,
            'word_count': 0.0,
        }
        score = 0.0
        score += weights['avg_word_length'] * (features.get('avg_word_length', 0) / 6.0)
        score += weights['type_token_ratio'] * features.get('type_token_ratio', 0)
        score += weights['punctuation_ratio'] * (features.get('punctuation_ratio', 0) * 10)
        score += weights['stopword_ratio'] * features.get('stopword_ratio', 0)
        score += weights['repeat_word_fraction'] * features.get('repeat_word_fraction', 0)
        return 1 / (1 + math.exp(-6 * (score - 0.0)))

    ensemble_scores = []
    for text, ml_prob in zip(X_val, probs):
        heuristic_prob = heuristic_prob_from_text(text)
        ensemble_scores.append((1.0 - 0.7) * heuristic_prob + 0.7 * ml_prob)

    precision, recall, thresholds = precision_recall_curve(y_val, ensemble_scores)
    best_threshold = 0.5
    best_f1 = -1.0

    for idx, threshold in enumerate(thresholds):
        if precision[idx] + recall[idx] == 0:
            continue
        f1 = 2 * precision[idx] * recall[idx] / (precision[idx] + recall[idx])
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(threshold)

    predictions = [1 if prob >= best_threshold else 0 for prob in ensemble_scores]
    return {
        'threshold': float(best_threshold),
        'accuracy': float(accuracy_score(y_val, predictions)),
        'precision': float(precision_score(y_val, predictions, zero_division=0)),
        'recall': float(recall_score(y_val, predictions, zero_division=0)),
        'f1': float(f1_score(y_val, predictions, zero_division=0)),
        'validation_size': len(y_val),
    }

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--calibrate', '-c', help='Path to CSV with text,label or text,generated columns to auto-calibrate')
    args = parser.parse_args()

    try:
        dataset_path = None
        if args.calibrate:
            dataset_path = args.calibrate
        elif os.path.exists(DEFAULT_LABELED_DATASET):
            dataset_path = DEFAULT_LABELED_DATASET

        if dataset_path:
            texts, labels = load_labeled_dataset(dataset_path)
            if is_sklearn_available():
                print(f'Training sklearn pipeline on labeled dataset: {dataset_path}')
                from sklearn.pipeline import FeatureUnion, make_pipeline
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.linear_model import LogisticRegression
                from joblib import dump

                features = FeatureUnion([
                    ("word_tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=4000, lowercase=True)),
                    ("char_tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000, lowercase=True)),
                ])
                pipeline = make_pipeline(
                    features,
                    LogisticRegression(max_iter=2000, class_weight='balanced')
                )
                pipeline.fit(texts, labels)
                model_path = os.path.join(ROOT, 'models', 'model.joblib')
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                dump(pipeline, model_path)
                print(f'Sklearn model trained and saved to {model_path}')

                calibration = calibrate_threshold(texts, labels)
                calibration_path = os.path.join(ROOT, 'models', 'calibration.json')
                with open(calibration_path, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(calibration, f, indent=2)
                print(f'Calibrated threshold {calibration["threshold"]:.3f} saved to {calibration_path}')
            else:
                from src.simple_classifier import train_from_dataset
                model_path = train_from_dataset(texts, labels)
                print(f'Simple model trained and saved to {model_path}')
        else:
            model_path = train_and_save_model()
            print(f'Model trained and saved to {model_path}')
    except RuntimeError as e:
        print(str(e))
    except Exception as e:
        print('Training failed:', e)

if __name__ == '__main__':
    main()
