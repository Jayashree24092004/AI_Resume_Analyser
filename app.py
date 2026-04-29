# ─────────────────────────────────────────────────────────────────────────────
# app.py  ·  Entry point — AI Resume Analyser (Offline Version)
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from dotenv import load_dotenv

from constants import PAGE_CONFIG
from styles.theme import inject_css
from utils.helpers import init_session_state, save_to_history
from components.sidebar import render_sidebar
from components.input_panel import render_input_panel
from components.results_panel import render_results
from utils.local_model import analyse_resume


# ── Bootstrap ─────────────────────────────────────────────────────────────────
load_dotenv()
st.set_page_config(**PAGE_CONFIG)
inject_css()
init_session_state()


# ── Sidebar (no API now) ──────────────────────────────────────────────────────
render_sidebar()


# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='padding: 8px 0 24px;'>
        <h1 style='font-size:32px; font-weight:800; letter-spacing:-1px; margin:0;'>
            🎯 AI Resume Analyser
        </h1>
        <p style='color:#7a7a9a; margin:4px 0 0; font-size:15px;'>
            Upload a resume · Paste a job description · Get instant offline AI insights
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── If result already exists, show it directly ────────────────────────────────
if st.session_state.result:
    render_results(st.session_state.result)
    st.stop()


# ── Input panel ───────────────────────────────────────────────────────────────
jd_text, resume_info = render_input_panel()

st.markdown("<br>", unsafe_allow_html=True)


# ── Analyse button (NO API condition now) ─────────────────────────────────────
ready = (
    len(jd_text.strip()) >= 30
    and resume_info is not None
    and (resume_info.get("text", "").strip() or resume_info.get("base64"))
)

col_btn, col_hint = st.columns([2, 5])

with col_btn:
    analyse_clicked = st.button(
        "🔍 Analyse Resume",
        disabled=not ready,
        use_container_width=True,
    )

with col_hint:
    if len(jd_text.strip()) < 30:
        st.info("Paste a job description (min 30 characters).", icon="📋")
    elif resume_info is None:
        st.info("Upload a resume or paste text above.", icon="📄")
    else:
        st.success("Ready — click Analyse Resume!", icon="✅")


# ── Run analysis ──────────────────────────────────────────────────────────────
if analyse_clicked and ready:
    with st.spinner("Analyzing resume using local AI model..."):
        result, error = analyse_resume(
            jd=jd_text,
            resume_text=resume_info.get("text", ""),
            pdf_base64=resume_info.get("base64"),
        )

    if error:
        st.error(f"❌ {error}", icon="🚨")
    elif result:
        st.session_state.result = result
        save_to_history(result)
        st.rerun()