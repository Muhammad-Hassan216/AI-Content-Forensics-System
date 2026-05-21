AI Content Forensics System

Detects whether text is AI-generated and explains reasoning behind detection. This repository contains a simple prototype for local demonstrations and a minimal UI.
This repository contains a compact, explainable system to detect AI‑generated text and present evidence in a polished UI for judges and reviewers.

Quick pointers:
- App entry: `app.py` — Streamlit UI (wide layout, premium presentation)
- CLI demo: `run_demo.py` — quick sample runs and `demo_output.json`
- Trainer: `scripts/train_model.py` — train / calibrate on labeled CSV (`--calibrate`)
- Batch server: `scripts/batch_server.py` — lightweight POST `/predict` service
- Models: `models/model.joblib` (sklearn) and `models/simple_model.json` (pure‑Python fallback)
- Labeled training data: `data/labeled_training_samples.csv`
- Documentation and judge assets: see `downloads/DOCUMENTATION.md`
Features (competition-ready)
Run (recommended):
```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m streamlit run app.py
```
- High-level explainable detection pipeline (feature extraction → heuristic detector → explainer)
If you need an offline install, use the `wheels/` folder and install with `--no-index --find-links`.
- Clean, presentation-focused UI with quick-samples and one-click demo flow
For judges: the Roman‑Urdu explainer is in `ROMAN_URDU_README.md` and a printable PDF is available via `scripts/markdown_to_pdf.py`.
- Reproducible environment: `requirements.txt` and `.env.example`
See `downloads/DOCUMENTATION.md` for architecture, libraries, setup checklist, and submission instructions.
- Deliverables-ready: `README.md`, `submission-checklist.md`, and `demo_script_template.md`

Why this approach?
- Rapid implementation: all components are Python-based to minimise integration overhead.
- Explainability: judges value interpretable reasoning; contributions chart shows why a verdict was reached.
- Presentation-first: UI and demo script designed to fit a 5-minute recording and live judge walkthrough.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Run the demo UI (Streamlit):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run app.py
```

If you prefer a single-step (using the workspace Python):

```bash
"C:/Program Files/Python313/python.exe" -m pip install -r requirements.txt
"C:/Program Files/Python313/python.exe" -m streamlit run app.py
```

Optional: train the lightweight classifier (recommended for better accuracy):

```bash
python scripts/train_model.py
```

This creates `models/model.joblib` which the app will load automatically if present.

Files created
- `app.py` — Streamlit demo launcher
- `src/feature_extractor.py` — feature extraction utilities
- `src/detector.py` — detection logic
- `src/explainer.py` — explainability helpers
- `.env.example` — example environment variables
- `requirements.txt` — Python deps
- `submission-checklist.md` — final deliverables checklist
- `demo_script_template.md` — 5-minute demo script template

Notes
- This is a prototype with heuristic detection intended for demonstration. Replace heuristics with a trained model for production accuracy.
