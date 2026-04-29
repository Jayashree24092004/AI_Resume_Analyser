# ─────────────────────────────────────────────────────────────────────────────
# styles/theme.py  ·  Global dark-theme CSS for Streamlit
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st


GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

/* ── Root override ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* ── Main block padding ── */
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1200px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #12121a !important;
    border-right: 1px solid #2a2a3e;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #e8e8f0 !important;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    color: #ffffff !important;
    letter-spacing: -0.5px;
}

/* ── Text areas / inputs ── */
textarea, input[type="text"], input[type="password"] {
    background: #12121a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
textarea:focus, input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px #6c63ff22 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #12121a;
    border: 2px dashed #2a2a3e;
    border-radius: 12px;
    padding: 12px;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #00cec9) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
}
.stButton > button:disabled {
    opacity: 0.4 !important;
    cursor: not-allowed !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #1a1a26 !important;
    border: 1px solid #2a2a3e !important;
    color: #a29bfe !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div {
    background: #12121a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #12121a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-width: 1px !important;
}

/* ── Divider ── */
hr {
    border-color: #2a2a3e !important;
    margin: 12px 0 !important;
}

/* ── Plotly charts bg ── */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #1a1a26 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #7a7a9a !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 700 !important; }

/* ── Caption text ── */
.stCaption { color: #7a7a9a !important; }

/* ── Spinner ── */
.stSpinner { color: #6c63ff !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6c63ff; }
</style>
"""

# ── Colours for COURSE_COLORS (needed by results_panel) ──────────────────────
COURSE_COLORS = [
    {"bg": "#6c63ff33", "text": "#a29bfe"},
    {"bg": "#00cec933", "text": "#00cec9"},
    {"bg": "#00b89433", "text": "#00b894"},
    {"bg": "#fdcb6e33", "text": "#fdcb6e"},
    {"bg": "#e1705533", "text": "#e17055"},
]


def inject_css():
    """Inject the global CSS into the Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)