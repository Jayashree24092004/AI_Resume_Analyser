# ─────────────────────────────────────────────────────────────────────────────
# components/sidebar.py  ·  Sidebar (Offline Version)
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from constants import JD_PRESETS
from utils.helpers import get_score_band, reset_analysis


def render_sidebar():
    with st.sidebar:

        # ── Logo / Title ─────────────────────────
        st.markdown(
            """
            <div style='text-align:center; padding: 8px 0 20px;'>
                <div style='font-size:40px;'>🎯</div>
                <h2 style='margin:6px 0 2px; font-size:18px; color:#e8e8f0;'>
                    AI Resume Analyser
                </h2>
                <p style='color:#7a7a9a; font-size:12px; margin:0;'>
                    Fully Offline · No API · No Cost
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── JD Presets ───────────────────────────
        st.markdown("**📋 Quick JD Presets**")
        preset_choice = st.selectbox(
            label="Load a sample job description",
            options=list(JD_PRESETS.keys()),
            label_visibility="collapsed",
        )

        if preset_choice != "— Select a preset JD —":
            if st.button("📥 Load this JD", use_container_width=True):
                st.session_state.jd = JD_PRESETS[preset_choice]
                st.rerun()

        st.divider()

        # ── Analysis History ─────────────────────
        history = st.session_state.get("history", [])
        st.markdown(f"**📂 Recent Analyses** ({len(history)})")

        if not history:
            st.caption("No analyses yet this session.")
        else:
            for i, h in enumerate(history):
                band = get_score_band(h["match_score"])
                color = {"green": "🟢", "orange": "🟡", "red": "🔴"}.get(
                    band["color"], "⚪"
                )

                st.markdown(
                    f"{color} **{h['name']}** — {h['match_score']}/100  \n"
                    f"<small style='color:#7a7a9a;'>"
                    f"{h['predicted_field']} · {h['experience_level']}"
                    f"</small>",
                    unsafe_allow_html=True,
                )

                if i < len(history) - 1:
                    st.markdown(
                        "<hr style='margin:6px 0; border-color:#2a2a3e;'>",
                        unsafe_allow_html=True,
                    )

        st.divider()

        # ── Reset Button ─────────────────────────
        if st.session_state.get("result"):
            if st.button("🔄 New Analysis", use_container_width=True):
                reset_analysis()
                st.rerun()

        # ── Footer ───────────────────────────────
        st.markdown(
            "<p style='color:#4a4a6a; font-size:11px; text-align:center; margin-top:20px;'>"
            "Runs locally · No API calls · No data stored"
            "</p>",
            unsafe_allow_html=True,
        )