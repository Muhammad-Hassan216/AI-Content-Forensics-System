# AI Content Forensics System — Quick Judge & Run Guide

This file summarizes the project, how it works, and step‑by‑step commands to run the demo, train models, and troubleshoot common issues. Use this to explain the project to judges or to run the system quickly on a machine.

---

## Project summary
- Purpose: detect whether input text is AI‑generated and provide an explainable justification (feature contributions + token highlights).
- Components:
  - Heuristic detector (`src/detector.py`) — weighted feature rules mapped to a sigmoid.
  - Lightweight ML classifier (`src/classifier.py`) — TF‑IDF + LogisticRegression if `scikit-learn` available; otherwise a pure‑Python Naive Bayes fallback (`src/simple_classifier.py`).
  - Feature extractor (`src/feature_extractor.py`) — tokenization and features like avg word length, type/token ratio, punctuation ratio, stopword ratio, repeat words.
  - Explainer (`src/explainer.py`) — maps detector weights to contributions and produces token‑level contributions.
  - Token highlighter (`src/token_highlighter.py`) — highlights repeated/long/stopword tokens for demo UI.
  - Streamlit UI (`app.py`) — polished demo with presets, batch upload, CSV export, and detailed view.
  - CLI demo (`run_demo.py`) — runs the pipeline and produces `demo_output.json`.
  - Batch HTTP server (`scripts/batch_server.py`) — POST `/predict` for programmatic use.
  - Training script (`scripts/train_model.py`) — trains sklearn pipeline when available, otherwise uses simple fallback; supports `--calibrate path.csv` to train on labeled CSV.
  - Demo launcher (`scripts/demo_launch.py`) — starts Streamlit and opens browser.

---

## Quick setup (Windows, uses existing venv `.venv-1`)
1. Activate venv:

```powershell
& ".venv-1\Scripts\Activate.ps1"
```

2. If you have network, install runtime deps (Streamlit, etc):

```powershell
python -m pip install --no-cache-dir streamlit matplotlib numpy python-dotenv
```

3. If network is unreliable, the project runs with the pure‑Python fallback classifier (already committed). You do not strictly need `scikit-learn` to demo.

---

## Run the Streamlit demo
- Interactive (local window will open):

```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m streamlit run app.py
```

- Headless (no onboarding prompt, for automated runs or recording):

```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m streamlit run app.py --server.headless true
```

The UI provides: input modes (Single / Multi‑line / Upload CSV), ensemble presets (Auto, Heuristic‑biased, ML‑biased, Custom), threshold slider, CSV export, and token highlighting.

---

## CLI demo (quick evidence for judges)

```powershell
& ".venv-1\Scripts\Activate.ps1"
python run_demo.py

# Output saved to demo_output.json
```

---

## Train / Auto‑calibrate
- Train default pipeline (sklearn if installed, otherwise simple model):

```powershell
& ".venv-1\Scripts\Activate.ps1"
python scripts\train_model.py
```

- Auto‑calibrate with labeled CSV (must have `text` and `label` columns; label 1 = AI, 0 = human):

```powershell
& ".venv-1\Scripts\Activate.ps1"
python scripts\train_model.py --calibrate path\to\labeled.csv
```

If `scikit-learn` is available this will train and save a sklearn pipeline to `models/model.joblib`. Otherwise the simple fallback model will be saved to `models/simple_model.json`.

---

## Batch server (programmatic predictions)

```powershell
& ".venv-1\Scripts\Activate.ps1"
python scripts\batch_server.py

# POST to http://localhost:8000/predict with JSON: {"texts": ["text1","text2"]}
```

Response JSON: `{"results": [{"label","ensemble","ml_prob","heuristic_prob"}, ...]}`

---

## Tuning for judges (fast tips)
- If a Gemini text is labeled `Human` but you expect `AI`, try:
  - Select `Ensemble preset` → `ML-biased` (gives ML stronger influence), or set `Custom` and move `ML weight` to ~0.85–0.95.
  - Lower `Detection threshold` (e.g., 0.30) to be more permissive for `AI` labeling during demo.
  - Use `scripts\train_model.py --calibrate` with a small labeled set of Gemini examples to improve ML accuracy.

---

## Files map (important files to reference)
- `app.py` — Streamlit UI
- `run_demo.py` — CLI demo (produces `demo_output.json`)
- `src/feature_extractor.py` — features
- `src/detector.py` — heuristic + ensemble logic
- `src/classifier.py` — sklearn pipeline wrapper + fallback loader
- `src/simple_classifier.py` — pure‑Python NB fallback, `train_from_dataset()` for calibration
- `src/explainer.py` — contributions + token contributions
- `src/token_highlighter.py` — token highlighting HTML
- `scripts/train_model.py` — training / calibrate
- `scripts/batch_server.py` — batch HTTP server
- `scripts/demo_launch.py` — launches UI

---

## Troubleshooting
- `SyntaxError: source code string cannot contain null bytes` — indicates a file contains a stray null; fixed version committed. If seen, re-open the file and ensure UTF‑8 encoding.
- `pip install` fails due to connection reset: use an internet machine to `pip download --dest wheels ...` and copy wheels; then install locally:

```powershell
# On internet machine (matching Python+platform):
python -m pip download --dest wheels scikit-learn==1.8.0 scipy==1.17.1 joblib==1.5.3 threadpoolctl==3.6.0 --only-binary=:all:

# Copy wheels folder to offline machine, then on offline machine:
& ".venv-1\Scripts\Activate.ps1"
python -m pip install --no-index --find-links="C:\path\to\wheels" scikit-learn scipy joblib threadpoolctl
```

- If installation fails due to MSVC, install Visual C++ Redistributable for Visual Studio.

---

## Quick checklist for a judges demo (2 minutes)
1. Activate venv.
2. Run `python scripts/demo_launch.py` (opens Streamlit) or run headless and open `http://localhost:8501`.
3. Paste a sample Gemini text, set `Ensemble preset` to `ML-biased`, set threshold to `0.30`, click `Analyze`.
4. Narrate features on the left, show contributions bar, then token highlights and final confidence.

---

If you want, I can also generate a one‑slide PDF with these steps and sample screenshots for the judges. Tell me if you want that and which screenshots to include.
