# Roman-Urdu Explainer — AI Content Forensics System

Yeh file app ko judges ke samne explain karne ke liye Roman-Urdu mein hai. Aap isko parh ke demo samjha sakte ho.

---

1) Project ka Maqsad (ek jumla):

- Hamara tool yeh batata hai ke dia gaya text AI‑generated hai ya human‑written, aur kyun — explainable features aur token highlighting dikhakar.

2) Overall Flow (seedha aur simple):

- Step 1: `extract_features(text)` — text se kuch simple numeric features nikalte hain (avg word length, type/token ratio, punctuation density, stopwords %, repeat words, word count).
- Step 2: `detector` — features ko weight deke ek heuristic score banata, phir sigmoid se probability banta (heuristic_prob).
- Step 3: Agar ML model maujood ho to `predict_proba(text)` ML probability (ml_prob) deta.
- Step 4: Final score = (1-ml_weight)*heuristic_prob + ml_weight*ml_prob; agar score threshold se upar hua to label `AI-generated` warna `Human-written`.
- Step 5: `explain()` — features ke contributions aur per-token contributions nikalta, token_highlighter un tokens ko color karta jin se model decision pe asar pada.

3) Important files aur unka kaam (short):

- `app.py` — Streamlit UI; sidebar pe threshold, presets, input mode; detailed view me contributions aur highlighted tokens dikhte.
- `run_demo.py` — simple CLI demo jo sample texts pe run karke `demo_output.json` bana deta.
- `src/feature_extractor.py` — features nikalta; raw_text bhi store karta token mapping ke liye.
- `src/detector.py` — heuristic score + ensemble logic (ml_weight adjustable).
- `src/classifier.py` — sklearn pipeline wrapper (agar scikit-learn install ho); warna `simple_classifier` fallback use karta.
- `src/simple_classifier.py` — pure Python Naive Bayes fallback (offline friendly), aur `train_from_dataset()` se calibrate kar sakte.
- `src/explainer.py` — feature contributions aur token_contributions banata.
- `src/token_highlighter.py` — highlighted HTML return karta for display.
- `scripts/train_model.py` — train / calibrate script; `--calibrate path.csv` se labeled data par train karega.
- `scripts/batch_server.py` — small HTTP server for programmatic predictions (POST /predict).
- `scripts/demo_launch.py` — ek command se Streamlit start karke browser khol deta.

4) Jaldi run commands (copy-paste kar ke chalana):

- Activate venv:
```powershell
& ".venv-1\Scripts\Activate.ps1"
```
- Run headless Streamlit (recommended for demo):
```powershell
python -m streamlit run app.py --server.headless true
```
- Agar terminal prompt aa raha ho to (onboarding), `Enter` press karo ya headless flag use karo.
- CLI demo (quick evidence):
```powershell
python run_demo.py
# output saved to demo_output.json
```
- Start batch server:
```powershell
python scripts\batch_server.py
# POST JSON {"texts": ["...","..."]} to http://localhost:8000/predict
```
- Auto‑calibrate with labeled CSV (text,label):
```powershell
python scripts\train_model.py --calibrate path\to\labeled.csv
```

5) Demo narration tips (bolne ke liye):

- "Yeh system do cheezon se faisla karta: seedha rule‑based features aur ek machine learning model. Dono ko mila kar final probability nikalte hain."
- "Left side pe features aur unki values dekhenge; beech me contribution chart batayega kaun se feature ka kitna asar hai; aur highlighted text se jaldi dikhla sakte hain kaun se lafz model‑jaisay lag rahe."
- "Agar koi text aapko AI lagta hai lekin label Human aa raha hai, main 'Ensemble preset' ko ML‑biased kar ke dikhata hoon ya threshold thoda kam kar deta hoon (e.g., 0.30)."

6) Agar scikit-learn install fail kare (network issue):

- Hamare paas pure‑Python fallback already hai (`models/simple_model.json`). Aap bina internet ke bhi demo chala sakte ho.
- Agar phir bhi sklearn chahte ho to wheels dusre machine se download karke local folder se install karo (steps README mein diye gaye hain). Main aapko exact filenames bhi de sakta hoon.

7) Quick troubleshooting lines (bol ke batao):

- "Agar Streamlit onboarding pooche to Enter press karo ya `--server.headless true` laga do."
- "Agar pip download break ho jaye to wheels method use karo: internet PC pe `pip download --dest wheels scikit-learn scipy joblib threadpoolctl`, phir offline machine pe `pip install --no-index --find-links=path\to\wheels ...`."

8) Ending sentence to say to judges:

- "Yeh demo fast, explainable aur reproducible hai — aap features, token highlights, aur model probability sab check kar sakte hain; agar chaho hum isko aur calibrate kar ke specific generator (jaise Gemini) ke against aur behtar bana sakte hain." 

---

File ready — agar chaho main yeh Roman‑Urdu text ek PDF bana kar download link ke liye prepare kar doon.
