import matplotlib.pyplot as plt
import streamlit as st

from src.detector import detect
from src.explainer import explain
from src.feature_extractor import extract_features
from src import classifier
from src.token_highlighter import highlight_tokens


st.set_page_config(page_title="AI Content Forensics System", page_icon="🔎", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --bg: #f4f6fb;
            --panel: rgba(255, 255, 255, 0.90);
            --panel-strong: #ffffff;
            --border: rgba(15, 23, 42, 0.08);
            --text: #0f172a;
            --muted: #667085;
            --accent: #1d4ed8;
            --accent-2: #0f766e;
            --accent-soft: rgba(29, 78, 216, 0.10);
            --shadow: 0 22px 52px rgba(15, 23, 42, 0.08);
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", "SF Pro Display", system-ui, sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(29, 78, 216, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.08), transparent 26%),
                linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.75rem;
            max-width: 1400px;
        }

        section[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.88);
            border-right: 1px solid var(--border);
            padding-top: 1rem;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.85rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-shell {
            background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(241,245,249,0.74));
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            border-radius: 28px;
            padding: 1.5rem 1.6rem 1.35rem;
            margin-bottom: 1.25rem;
        }

        .hero-kicker {
            font-size: 0.82rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .hero-title {
            font-size: 2.5rem;
            line-height: 1.05;
            font-weight: 800;
            color: var(--text);
            margin: 0;
        }

        .hero-copy {
            margin-top: 0.65rem;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
            max-width: 980px;
        }

        .section-label {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-weight: 700;
            color: var(--accent);
            margin: 0 0 0.35rem 0;
        }

        .panel-card {
            background: var(--panel);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            border-radius: 22px;
            padding: 1.15rem 1.15rem 1rem;
            height: 100%;
        }

        .panel-card.strong {
            background: var(--panel-strong);
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-bottom: 1rem;
        }

        .metric-card {
            border-radius: 18px;
            border: 1px solid rgba(37, 99, 235, 0.12);
            background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(248,250,252,0.98));
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
            padding: 1rem 1rem 0.9rem;
            min-height: 108px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.09em;
        }

        .metric-value {
            color: var(--text);
            font-size: 2rem;
            font-weight: 800;
            line-height: 1;
            margin-top: 0.45rem;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: 0.3rem;
        }

        .badge-pill {
            padding: 0.9rem 1rem;
            border-radius: 16px;
            font-size: 1.05rem;
            font-weight: 800;
            text-align: center;
            color: #fff;
            box-shadow: 0 14px 32px rgba(37, 99, 235, 0.18);
        }

        .sidebar-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 0.45rem;
        }

        .sidebar-note {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.55;
            margin-bottom: 0.75rem;
        }

        .compact-rule {
            border-top: 1px solid rgba(15, 23, 42, 0.09);
            margin: 0.9rem 0;
        }

        .feature-box {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        }

        .feature-box pre {
            white-space: pre-wrap;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def metric_card(label, value, note="", accent="#2563eb"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{accent}">{value}</div>
            {f'<div class="metric-note">{note}</div>' if note else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-kicker">Production Application</div>
        <h1 class="hero-title">AI Content Forensics System</h1>
        <div class="hero-copy">
            <strong>Purpose:</strong> AI-generated text detection with explainable evidence, premium presentation, and a clean workflow for judges, reviewers, and live walkthroughs.
            Use the sidebar to load curated samples, upload batches, or paste your own text. Click <em>Analyze</em> to run predictions.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

sample_texts = {
    "Human-like": (
        "I wrote this after checking the source twice and then compared the results "
        "with the original note."
    ),
    "AI-like": (
        "This comprehensive analysis highlights the multifaceted implications of the "
        "proposed framework in a concise and structured manner."
    ),
    "Long AI-like (demo)": (
        """
        In recent years, rapid advancements in generative models have produced highly coherent
        and contextually relevant text. This example demonstrates verbosity, formal phrasing,
        and low punctuation density commonly found in model-generated outputs.
        """
    ),
}

with st.sidebar:
    st.markdown('<div class="sidebar-title">Application Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-note">Compact controls for sample loading, sensitivity tuning, and ensemble adjustment.</div>', unsafe_allow_html=True)
    sample_choice = st.selectbox("Load sample text", ["Custom", *sample_texts.keys()])
    threshold = st.slider("Detection threshold", 0.0, 1.0, 0.5)
    st.markdown('<div class="compact-rule"></div>', unsafe_allow_html=True)
    preset = st.selectbox("Ensemble preset", ["Auto", "Heuristic-biased", "ML-biased", "Custom"])
    if preset == 'Auto':
        ml_weight = 0.7
    elif preset == 'Heuristic-biased':
        ml_weight = 0.2
    elif preset == 'ML-biased':
        ml_weight = 0.85
    else:
        ml_weight = st.slider("ML weight in ensemble", 0.0, 1.0, 0.7)
    st.markdown('<div class="compact-rule"></div>', unsafe_allow_html=True)
    input_mode = st.selectbox("Input mode", ["Single", "Multi-line", "Upload CSV"])
    sample_quick_run = st.checkbox("Auto-run on load (use for recording)", value=False)
    st.markdown("---")
    st.write("Recommended: use `Long AI-like` during walkthrough to show charts and feature contributions.")

default_text = sample_texts.get(sample_choice, "") if sample_choice != "Custom" else ""

# Main input area adapts to chosen mode
if input_mode == "Upload CSV":
    uploaded = st.file_uploader("Upload CSV/TXT with a `text` column or one text per line", type=["csv", "txt"])
    text = ""
else:
    placeholder = "Paste text here" if input_mode == "Single" else "Paste multiple texts separated by a blank line (\n\n)"
    text = st.text_area(placeholder, value=default_text, height=320)

col1, col2 = st.columns([1.2, 0.8], gap="large")
with col1:
    analyze_clicked = st.button("Analyze")
    with col2:
        st.write("Presentation flow: input → analyze → evidence → decision")

if sample_quick_run and sample_choice != "Custom":
    analyze_clicked = True

def run_analysis(text, threshold, ml_weight):
    features = extract_features(text)
    detection = detect(features, text=text, threshold=threshold, ml_weight=ml_weight)
    explanation = explain(features, detection)
    return features, detection, explanation

if analyze_clicked:
    # collect texts depending on mode
    texts = []
    if input_mode == "Upload CSV":
        if uploaded is None:
            st.warning("Please upload a file first.")
            st.stop()
        else:
            import io, csv
            content = uploaded.read().decode('utf-8')
            # try CSV with header
            try:
                reader = csv.DictReader(io.StringIO(content))
                if 'text' in reader.fieldnames:
                    for row in reader:
                        if row.get('text'):
                            texts.append(row['text'])
                else:
                    # fallback: take first column
                    for row in reader:
                        first = list(row.values())[0]
                        if first:
                            texts.append(first)
            except Exception:
                # plain text file: split by blank lines
                parts = [p.strip() for p in content.split('\n\n') if p.strip()]
                texts.extend(parts)
    elif input_mode == "Multi-line":
        parts = [p.strip() for p in text.split('\n\n') if p.strip()]
        texts = parts
    else:
        if not text.strip():
            st.warning("Please provide input text.")
            st.stop()
        texts = [text.strip()]

    results = []
    for t in texts:
        features, detection, explanation = run_analysis(t, threshold, ml_weight)
        results.append({
            'text': t,
            'label': detection.get('label'),
            'ensemble': detection.get('score'),
            'ml_prob': detection.get('ml_prob'),
            'heuristic_prob': detection.get('heuristic_prob'),
            'word_count': features.get('word_count'),
            'contributions': explanation.get('contributions')
        })

    # Display summary table
    st.subheader("Predictions")
    import pandas as _pd
    df = _pd.DataFrame([{k: ('' if v is None else v) for k, v in r.items() if k != 'contributions'} for r in results])
    # shorten text for table
    df_display = df.copy()
    df_display['text'] = df_display['text'].apply(lambda s: (s[:140] + '...') if len(s) > 140 else s)
    st.dataframe(df_display)

    # counts
    counts = df['label'].value_counts().to_dict()
    st.markdown(f"**Counts:** {counts}")

    # allow download CSV
    import io, csv
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(['text', 'label', 'ensemble', 'ml_prob', 'heuristic_prob', 'word_count'])
    for r in results:
        writer.writerow([r['text'], r['label'], r['ensemble'], r['ml_prob'], r['heuristic_prob'], r['word_count']])
    st.download_button('Download results CSV', data=csv_buf.getvalue(), file_name='predictions.csv', mime='text/csv')

    # if single input, show full explanation and chart
    if len(results) == 1:
        r = results[0]
        st.subheader('Detailed result')
        st.markdown('---')
        c1, c2 = st.columns([1.05, 0.95], gap="large")
        with c1:
            st.markdown('<div class="section-label">Text + Features</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-card strong">', unsafe_allow_html=True)
            st.markdown('**Full text**')
            highlighted = highlight_tokens(r['text'])
            st.markdown(highlighted, unsafe_allow_html=True)
            st.markdown('---')
            st.markdown('**Extracted features**')
            st.json(explain(extract_features(r['text']), {'label': r['label'], 'score': r['ensemble']} )['contributions'])
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="section-label">Decision Summary</div>', unsafe_allow_html=True)
            color = '#0f766e' if 'AI' in (r['label'] or '') else '#1d4ed8'
            badge = f"<div class='badge-pill' style='background:{color}'>{r['label']}</div>"
            st.markdown(badge, unsafe_allow_html=True)
            st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)

            metric_cols = st.columns(3, gap="small")
            with metric_cols[0]:
                metric_card('Ensembled confidence', f"{r['ensemble']:.2%}", 'Final score after heuristic + ML fusion', '#2563eb')
            with metric_cols[1]:
                metric_card('ML model AI prob', f"{r['ml_prob']:.2%}" if r['ml_prob'] is not None else 'N/A', 'Direct classifier output', '#0f766e')
            with metric_cols[2]:
                metric_card('Heuristic prob', f"{r['heuristic_prob']:.2%}" if r['heuristic_prob'] is not None else 'N/A', 'Rule-based baseline score', '#7c3aed')

            st.markdown('---')
            st.markdown('<div class="section-label">Chart</div>', unsafe_allow_html=True)
            contrib = r['contributions'] or {}
            labels = list(contrib.keys())
            values = [contrib[k]['raw'] for k in labels]
            fig, ax = plt.subplots(figsize=(6.8, 3.3))
            colors = ["#1d4ed8" if v >= 0 else "#0f766e" for v in values]
            ax.bar(labels, values, color=colors)
            ax.axhline(0, color="black", linewidth=0.7)
            ax.set_ylabel('Contribution')
            ax.tick_params(axis='x', rotation=20)
            fig.tight_layout()
            st.pyplot(fig, clear_figure=True)
