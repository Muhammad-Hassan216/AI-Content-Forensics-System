# AI Content Forensics System

A fast, explainable Python demo that estimates whether a piece of text is AI-generated and shows the reasoning behind the decision.

The project is tuned for hackathon demos and judge walkthroughs: it ships with a polished Streamlit UI, a CLI demo, a lightweight batch endpoint, and both trained and pure-Python fallback models.

## What is included

- `app.py` - Streamlit UI with explainability, batch input, and export support
- `run_demo.py` - CLI demo that writes `demo_output.json`
- `scripts/train_model.py` - train or calibrate on `text,label` CSV data
- `scripts/batch_server.py` - lightweight POST `/predict` endpoint for batch checks
- `models/model.joblib` - sklearn model, when trained
- `models/simple_model.json` - pure-Python fallback model for offline use
- `data/labeled_training_samples.csv` - small labeled dataset kept for calibration/demo only
- `AI Generated Essays Dataset.csv` - larger Kaggle dataset used as the default training source
- `downloads/DOCUMENTATION.md` - setup, architecture, testing, and submission notes
- `ROMAN_URDU_README.md` - judge-friendly Roman-Urdu explainer

## Why this design

- Explainable: the app shows feature contributions and token highlights, not just a label
- Practical: it works online with sklearn and offline with the fallback classifier
- Demo-ready: the UI and docs are structured for a short, live presentation

## Quick start

Activate the virtual environment and run the app:

```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m streamlit run app.py
```

If you want the CLI demo instead:

```powershell
& ".venv-1\Scripts\Activate.ps1"
python run_demo.py
```

To train or recalibrate on labeled data:

```powershell
& ".venv-1\Scripts\Activate.ps1"
python scripts\train_model.py
```

If you want to recalibrate on the small local CSV instead:

```powershell
python scripts\train_model.py --calibrate data\labeled_training_samples.csv
```

The Kaggle dataset run also saves a calibration snapshot to `models/calibration.json` for reference.

To run batch predictions:

```powershell
& ".venv-1\Scripts\Activate.ps1"
python scripts\batch_server.py
```

Then POST JSON like `{"texts": ["sample 1", "sample 2"]}` to `http://localhost:8000/predict`.

## Offline install

If network access is unstable, install from the bundled wheels folder:

```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m pip install --no-index --find-links="wheels" scikit-learn scipy joblib threadpoolctl
```

## Documentation

- Architecture, setup, and submission checklist: `downloads/DOCUMENTATION.md`
- Judge script and demo flow: `demo_script_template.md`
- Final handoff checklist: `submission-checklist.md`

## Deploy

### Option 1: Render (recommended)

This repository now includes `render.yaml`, `Procfile`, and `runtime.txt`.

1. Push this repo to GitHub.
2. In Render, create a new Web Service from the repo.
3. Render auto-detects `render.yaml`; if prompted manually use:
	- Build command: `pip install -r requirements.txt`
	- Start command: `streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT`
4. Deploy and open the generated URL.

### Option 2: Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Set:
	- Main file path: `app.py`
	- Python version: `3.11`
4. Deploy.

### Local production-like run

```powershell
python -m streamlit run app.py --server.headless true --server.port 8501
```

## Notes

- This repository is a prototype for demos and judging, not a production-grade detector.
- Accuracy improves when you add more labeled examples and retrain with `scripts/train_model.py`.
