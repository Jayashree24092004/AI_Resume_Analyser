# ─────────────────────────────────────────────────────────────────────────────
# components/input_panel.py  ·  Job description + resume upload UI
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from constants import ACCEPTED_FILE_TYPES
from utils.file_parser import parse_uploaded_file
from utils.helpers import format_file_size


def render_input_panel() -> tuple[str, dict | None]:
    """
    Render the two-column input panel.

    Returns:
        (jd_text, resume_info_dict | None)
    """
    col_jd, col_resume = st.columns(2, gap="large")

    # ── Left: Job Description ─────────────────────────────────────────────────
    with col_jd:
        st.markdown("### 📋 Job Description")
        st.caption("Paste the full job description — skills, requirements, responsibilities.")

        jd_text = st.text_area(
            label="Job Description",
            value=st.session_state.get("jd", ""),
            height=300,
            placeholder=(
                "e.g. We are looking for a Data Scientist with expertise in "
                "Python, machine learning, and SQL...\n\n"
                "Or load a preset from the sidebar →"
            ),
            label_visibility="collapsed",
            key="jd_input",
        )
        # Keep session state in sync
        st.session_state.jd = jd_text

        char_count = len(jd_text.strip())
        if char_count == 0:
            st.caption("Minimum 30 characters required.")
        elif char_count < 30:
            st.warning(f"Too short ({char_count} chars). Please add more detail.")
        else:
            st.caption(f"✓ {char_count:,} characters")

    # ── Right: Resume Upload ──────────────────────────────────────────────────
    with col_resume:
        st.markdown("### 📄 Resume")
        st.caption("Upload PDF, DOCX, or TXT — or paste text below.")

        uploaded_file = st.file_uploader(
            label="Upload Resume",
            type=ACCEPTED_FILE_TYPES,
            label_visibility="collapsed",
            help="Supported: PDF, DOCX, TXT",
        )

        resume_info = None

        if uploaded_file is not None:
            with st.spinner("Reading file..."):
                resume_info = parse_uploaded_file(uploaded_file)

            # File metadata card
            st.success(
                f"**{resume_info['filename']}** loaded ✓  \n"
                f"Size: {format_file_size(resume_info['file_size'])} · "
                f"Pages: {resume_info['num_pages']} · "
                f"Type: {resume_info['ext'].upper()}",
                icon="📄",
            )

            if not resume_info["text"].strip():
                st.warning(
                    "Could not extract text from this file. "
                    "Try pasting the resume text below.",
                    icon="⚠️",
                )

        # Paste fallback
        with st.expander("✏️ Or paste resume text directly", expanded=(uploaded_file is None)):
            pasted_text = st.text_area(
                label="Resume Text",
                height=200,
                placeholder="Paste your resume content here...",
                label_visibility="collapsed",
                key="pasted_resume",
            )
            if pasted_text.strip():
                if resume_info is None:
                    resume_info = {
                        "text":      pasted_text,
                        "base64":    None,
                        "is_pdf":    False,
                        "num_pages": 1,
                        "file_size": len(pasted_text.encode()),
                        "filename":  "pasted_text.txt",
                        "ext":       "txt",
                    }
                else:
                    # Supplement extracted text if file text was empty
                    if not resume_info["text"].strip():
                        resume_info["text"] = pasted_text

    return jd_text, resume_info