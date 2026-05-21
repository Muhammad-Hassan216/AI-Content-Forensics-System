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


DEFAULT_LABELED_DATASET = os.path.join(ROOT, 'data', 'labeled_training_samples.csv')


def load_labeled_dataset(csv_path):
    texts = []
    labels = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or 'text' not in reader.fieldnames or 'label' not in reader.fieldnames:
            raise RuntimeError('CSV must have text and label columns')
        for row in reader:
            text = (row.get('text') or '').strip()
            label = (row.get('label') or '').strip()
            if text and label in {'0', '1'}:
                texts.append(text)
                labels.append(int(label))
    if not texts:
        raise RuntimeError(f'No valid labeled rows found in {csv_path}')
    return texts, labels

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--calibrate', '-c', help='Path to CSV with text,label columns to auto-calibrate')
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
