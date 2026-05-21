# AI Content Forensics System — Project Overview

This file documents the repository, how the detection pipeline works, how to run the demo (CLI + Streamlit), troubleshooting tips, and quick actions you can perform during the hackathon.

---

## Goal
- Provide a fast, explainable demo that detects whether text is AI-generated and explains the reasons (feature contributions + token highlighting).

## Quick status
- Streamlit UI implemented in `app.py` (polished UI with batch upload, presets, CSV export).
- Fallback CLI demo `run_demo.py` works without heavy third-party installs.
- Two classifier modes:
  - sklearn TF‑IDF + LogisticRegression pipeline (optional, needs scikit-learn).
  - pure‑Python Multinomial Naive Bayes fallback (`src/simple_classifier.py`) — works offline and is already saved at `models/simple_model.json`.

---

## Quickstart commands (Windows / PowerShell)
1) Activate venv:
```powershell
& ".venv-1\Scripts\Activate.ps1"
```

2) Run CLI demo (no network required):
```powershell
python run_demo.py
```

3) Run Streamlit UI (headless recommended if terminals are shared):
```powershell
python -m streamlit run app.py --server.headless true
```

4) Launch demo (auto open browser):
```powershell
python scripts\demo_launch.py
```

5) Start lightweight batch server (programmatic predictions):
```powershell
python scripts\batch_server.py
# POST to http://localhost:8000/predict with JSON {"texts": ["...","..."]}
```

6) Train / Auto-calibrate model from labeled CSV (`text,label`):
```powershell
# CSV must contain header columns: text,label (label 0=human,1=ai)
python scripts\train_model.py --calibrate path\to\labeled.csv
```

---

## File map & responsibilities
- `app.py` — Streamlit UI, controls (threshold, ensemble preset, batch upload), result display and token highlighting.
- `run_demo.py` — CLI demo that runs extract -> detect -> explain and writes `demo_output.json`.
- `scripts/train_model.py` — trains sklearn pipeline (if available) or falls back to simple trainer; supports `--calibrate`.
- `scripts/demo_launch.py` — starts Streamlit and opens browser (single-command for judges).
- `scripts/batch_server.py` — small HTTP server for batch JSON predictions.
- `src/feature_extractor.py` — tokenization and hand-crafted features: avg_word_length, type_token_ratio, punctuation_ratio, stopword_ratio, repeat_word_fraction, word_count (also stores `raw_text`).
- `src/detector.py` — combines heuristic score and optional ML probability into an ensemble; param `ml_weight` controls contribution.
- `src/explainer.py` — maps heuristic weights to feature contributions and computes naive per-token contributions; returns `contributions` and `token_contributions`.
- `src/classifier.py` — sklearn pipeline trainer/load/predict wrappers and logic to fallback to `simple_classifier` when sklearn not available.
- `src/simple_classifier.py` — pure‑Python Multinomial Naive Bayes trainer/load/predict for offline use.
- `src/token_highlighter.py` — small helper that returns HTML with repeated/long/stopword tokens highlighted.
- `models/` — place saved models here: `simple_model.json` (fallback) and `model.joblib` (sklearn pipeline if trained).
- `tests/` — basic unit tests (feature extractor, detector, simple classifier).
- `requirements.txt` — recommended packages; network-heavy (streamlit, matplotlib, numpy, scikit-learn optional).

---

## How detection works (short)
1. `extract_features(text)` computes a small set of interpretable features.
2. `detector.detect()` computes a heuristic score (weighted sum → sigmoid) → `heuristic_prob`.
3. If an ML model is available, `predict_proba(text)` returns `ml_prob`.
4. `final_prob = (1-ml_weight)*heuristic_prob + ml_weight*ml_prob` (default Auto preset gives ML priority).
5. `explain()` returns per-feature contributions and token-level contributions for presenting to judges.

Decision thresholds and `ml_weight` are adjustable in the UI (sidebar) so you can tune sensitivity for the demo.

---

## Why text labeled Human even if Gemini generated it
- The ensemble decision depends on threshold and both heuristic and ML probabilities. If both probabilities are below threshold (default 0.5), label is `Human-written`.
- Quick fixes during demo: set `Ensemble preset` → `ML-biased` (stronger ML influence) and/or lower `Detection threshold` to label more text as AI.

---

## Offline install (download wheels on another machine)
1) On an internet machine (matching OS and Python 3.13):
```powershell
mkdir wheels
python -m pip download --dest wheels scikit-learn==1.8.0 scipy==1.17.1 joblib==1.5.3 threadpoolctl==3.6.0
```
2) Copy the `wheels` folder to the offline machine and install:
```powershell
& ".venv-1\Scripts\Activate.ps1"
python -m pip install --no-index --find-links="C:\full\path\to\wheels" scikit-learn scipy joblib threadpoolctl
```
3) Verify:
```powershell
python -c "import sklearn, scipy, joblib; print(sklearn.__version__, scipy.__version__, joblib.__version__)"
```

Notes:
- Make sure wheel filenames include the tag `cp313` and `win_amd64` for Python 3.13 on Windows. If tags differ (e.g. cp310), the wheel won't install.
- If `scipy` download is failing, try on a stable connection — the wheel is large (~30–40MB).
- If pip complains about missing C runtime when installing, install Visual C++ Redistributable for Visual Studio.

---

## Troubleshooting common issues
- Streamlit onboarding prompt: When running `python -m streamlit run app.py` Streamlit may ask for email — press Enter or run with `--server.headless true`.
- SyntaxError due to null bytes (rare): If Python raises `source code string cannot contain null bytes`, open the file mentioned (we fixed `src/token_highlighter.py`) and ensure it's UTF-8 without nulls.
- Network errors during pip: use offline wheel method above.
- If a module import fails, check venv activation and `pip install -r requirements.txt` (or install minimal packages manually).

---

## Quick checklist for judges (one-minute script)
1. Activate venv.
2. Run `python scripts\demo_launch.py` to open UI.
3. Use `Long AI-like (demo)` sample and show features → contributions → token highlighting.
4. Toggle `Ensemble preset` between `Heuristic-biased` and `ML-biased` to show effect.
5. Upload a CSV with multiple texts and show table + Download CSV.

---

If you want, I can also create a single runnable ZIP with wheels included (you would still need to copy it to the target machine). Tell me if you want the exact wheel filenames for Python 3.13 on Windows and I will list them here.

Last updated: May 21, 2026
