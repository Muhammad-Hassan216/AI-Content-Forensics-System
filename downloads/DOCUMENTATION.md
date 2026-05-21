# Documentation — AI Content Forensics System

This document summarizes architecture, chosen libraries, setup & run steps, calibration instructions, testing, and the final submission checklist.

---

## 1. Project Overview

- Purpose: Detect whether a text is AI‑generated and provide explainable evidence (feature contributions and token highlights).
- Audience: Hackathon judges, reviewers, and researchers who need a fast, interpretable detector.

## 2. Architecture (high level)

- UI: `app.py` — Streamlit wide layout, sidebar controls, single/batch input modes, and a detailed result panel. Uses `src/token_highlighter.py` for token highlights.
- Feature extraction: `src/feature_extractor.py` — computes interpretable features (avg word length, type/token ratio, punctuation ratio, stopword ratio, repeat word fraction, word_count).
- Heuristic detector: `src/detector.py` — maps features to a heuristic probability via weighted sum + sigmoid.
- Classifier: `src/classifier.py` — trains/loads either a sklearn TF‑IDF + LogisticRegression pipeline (`models/model.joblib`) or falls back to `src/simple_classifier.py` which is a pure‑Python Naive Bayes saved at `models/simple_model.json`.
- Explainer: `src/explainer.py` — computes feature contributions and token contributions for explainability.
- Batch: `scripts/batch_server.py` — lightweight HTTP endpoint for programmatic predictions (POST `/predict`).

## 3. Key files

- `app.py` — Streamlit application (entry point).
- `scripts/train_model.py` — train / calibrate script. Use `--calibrate path/to/labeled.csv`.
- `run_demo.py` — CLI demo that saves `demo_output.json`.
- `models/` — saved models (`model.joblib` for sklearn, `simple_model.json` for fallback).
- `wheels/` — optional offline wheel files for Windows Python 3.13 (use `pip install --no-index --find-links=...`).
- `ROMAN_URDU_README.md` — Roman‑Urdu explainer for judges; printable via `scripts/markdown_to_pdf.py`.

## 4. Setup & Run (Windows example)

1. Create & activate venv (PowerShell):
```powershell
python -m venv .venv-1
& ".venv-1\Scripts\Activate.ps1"
```
2. Install dependencies (online):
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
3. Run Streamlit app:
```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m streamlit run app.py
```
4. Train / calibrate model on labeled CSV (optional):
```powershell
python scripts\train_model.py --calibrate path\to\labeled.csv
```

Offline wheels: if network unstable, download wheel files on another machine and install locally:
```powershell
python -m pip install --no-index --find-links="C:\path\to\wheels" scikit-learn scipy joblib
```

## 5. Improving accuracy (practical steps)

1. Collect representative labeled data (20–200 samples per class minimum). CSV format: `text,label` where `label` is `0` (human) or `1` (ai).
2. Run `python scripts\train_model.py --calibrate labeled.csv` to retrain sklearn pipeline (if scikit-learn installed) or update fallback model via `train_from_dataset()`.
3. Evaluate with a held-out test set and adjust `ml_weight` or ensemble threshold.
4. Optional: augment features (readability scores, POS tag distributions, perplexity from small LM) for greater robustness.

## 6. Testing & QA

- Unit tests: run `python -m pytest -q` (tests located in `tests/`).
- Quick sanity: `python scripts\run_sample_analysis.py` to reproduce sample scores.

## 7. Submission checklist (adjust to meet hackathon rules)

- README.md with project overview — present.
- `requirements.txt` — present.
- Setup & Run guide — present in README and here.
- Clean folder structure with `src/` — present.
- `.env.example` — present.
- GitHub repo with commits & branch — please push before deadline.
- Documentation: `downloads/DOCUMENTATION.md` and `PROJECT_OVERVIEW.md` — present.
- 5-minute screen recording with voice-over — to be recorded by team (script below).
- Final push to GitHub between 4:00–5:00 PM — coordinate and push now.

## 8. Demo recording script (5 minutes)

1. 0:00–0:20 — One‑line project goal and interface overview.
2. 0:20–1:20 — Paste an AI example, Analyze, show token highlights and metrics.
3. 1:20–2:20 — Paste a human example, show contrast in features and final label.
4. 2:20–3:20 — Upload CSV batch and download results.
5. 3:20–4:20 — Explain model architecture (TF‑IDF + LR & fallback), how to calibrate, and where code lives.
6. 4:20–5:00 — Closing remarks and where to find docs and repo link.

## 9. Contact / Next steps

If you want, I can:
- create a ZIP release with code + models,
- prepare a short Git commit message and run the final push for you,
- or retrain on any labeled CSV you upload.

Files placed in this folder:
- `downloads/DOCUMENTATION.md` (this file)
