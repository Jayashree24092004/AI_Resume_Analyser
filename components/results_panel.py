# ─────────────────────────────────────────────────────────────────────────────
# components/results_panel.py  ·  Display analysis results
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from constants import RESUME_SECTIONS, COLORS, COURSE_COLORS
from utils.helpers import get_score_band, get_field_color, score_color_hex, skill_list_to_csv

# ── Helper: colored badge HTML ────────────────────────────────────────────────
def _badge(text: str, bg: str, fg: str = "#ffffff") -> str:
    return (
        f"<span style='background:{bg}22; border:1px solid {bg}55; "
        f"color:{bg}; padding:3px 12px; border-radius:99px; "
        f"font-size:12px; font-weight:600;'>{text}</span>"
    )


# ── Score gauge (plotly) ──────────────────────────────────────────────────────
def _render_score_gauge(score: int):
    color = score_color_hex(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": "/100", "font": {"size": 32, "color": color}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#2a2a3e", "tickwidth": 1},
                "bar":  {"color": color, "thickness": 0.25},
                "bgcolor": "#1a1a26",
                "borderwidth": 0,
                "steps": [
                {"range": [0,   45], "color": "rgba(225,112,85,0.15)"},
                {"range": [45,  75], "color": "rgba(253,203,110,0.15)"},
                {"range": [75, 100], "color": "rgba(0,184,148,0.15)"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 3},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=220,
        margin=dict(t=20, b=10, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8e8f0",
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Skill radar chart ─────────────────────────────────────────────────────────
def _render_skill_radar(result: dict):
    sections = result.get("resume_sections", {})
    cats  = [RESUME_SECTIONS.get(k, k) for k in sections]
    vals  = [1 if v else 0 for v in sections.values()]

    total_skills   = max(len(result.get("extracted_skills", [])), 1)
    matched_skills = len(result.get("matched_skills", []))
    skill_pct      = round((matched_skills / total_skills) * 100)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=cats,
            y=vals,
            marker_color=[COLORS["green"] if v else COLORS["red"] for v in vals],
            text=["✓ Present" if v else "✗ Missing" for v in vals],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=dict(text="Resume Sections", font=dict(color="#e8e8f0", size=14)),
        height=260,
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showticklabels=False, showgrid=False, range=[0, 1.4]),
        xaxis=dict(tickfont=dict(color="#7a7a9a", size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Skills match donut ────────────────────────────────────────────────────────
def _render_skills_donut(result: dict):
    total   = len(result.get("extracted_skills", []))
    matched = len(result.get("matched_skills",   []))
    missing = len(result.get("missing_skills",   []))
    unmatched = max(0, total - matched)

    if total == 0 and missing == 0:
        st.caption("No skill data to chart.")
        return

    labels = ["Matched Skills", "Other Skills", "Missing Skills"]
    values = [matched, unmatched, missing]
    colors = [COLORS["green"], COLORS["muted"], COLORS["red"]]

    fig = px.pie(
        names=labels, values=values,
        color_discrete_sequence=colors,
        hole=0.55,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    fig.update_layout(
        title=dict(text="Skills Overview", font=dict(color="#e8e8f0", size=14)),
        height=260,
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8e8f0",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Main render ───────────────────────────────────────────────────────────────
def render_results(result: dict):
    score  = result.get("match_score", 0)
    band   = get_score_band(score)
    fcolor = get_field_color(result.get("predicted_field", "General"))

    # ── Header row ───────────────────────────────────────────────────────────
    st.markdown("---")
    h_col1, h_col2 = st.columns([3, 1])

    with h_col1:
        st.markdown(
            f"## {result.get('name', 'Unknown')} &nbsp;"
            + _badge(result.get("predicted_field", ""), fcolor)
            + "&nbsp;"
            + _badge(result.get("experience_level", ""), COLORS["accent"]),
            unsafe_allow_html=True,
        )
        email = result.get("email", "N/A")
        phone = result.get("phone", "N/A")
        st.caption(
            f"📧 {email}   |   📞 {phone}"
        )

    with h_col2:
        st.markdown(
            f"<div style='text-align:right; padding-top:8px;'>"
            f"<span style='color:{band['color']}; font-weight:700; font-size:16px;'>"
            f"{band['label']}</span></div>",
            unsafe_allow_html=True,
        )
        st.caption(band["message"])

    # ── Overall summary ───────────────────────────────────────────────────────
    summary = result.get("overall_summary", "")
    if summary:
        st.info(f"💬 {summary}", icon="🤖")

    # ── Score + Charts row ────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🎯 Match Score")
        _render_score_gauge(score)
    with c2:
        st.markdown("#### 📑 Resume Sections")
        _render_skill_radar(result)
    with c3:
        st.markdown("#### 🧠 Skills Breakdown")
        _render_skills_donut(result)

    # ── Skills detail ─────────────────────────────────────────────────────────
    st.markdown("### 🔍 Skills Analysis")
    sk1, sk2, sk3 = st.columns(3)

    with sk1:
        st.markdown("**All Extracted Skills**")
        skills = result.get("extracted_skills", [])
        matched = set(result.get("matched_skills", []))
        if skills:
            chips = " ".join(
                f"<span style='background:{COLORS['accent']}22; border:1px solid {COLORS['accent']}44; "
                f"color:{COLORS['accent'] if s in matched else COLORS['muted']}; "
                f"padding:3px 10px; border-radius:99px; font-size:12px; "
                f"display:inline-block; margin:2px;'>"
                f"{'✓ ' if s in matched else ''}{s}</span>"
                for s in skills
            )
            st.markdown(chips, unsafe_allow_html=True)
            st.caption(f"Purple = matched with JD · {len(matched)}/{len(skills)} matched")
        else:
            st.caption("No skills detected.")

    with sk2:
        st.markdown("**✅ Matched with JD**")
        for s in result.get("matched_skills", []):
            st.markdown(
                f"<span style='color:{COLORS['green']}; font-size:13px;'>✓ {s}</span>",
                unsafe_allow_html=True,
            )
        if not result.get("matched_skills"):
            st.caption("No skill matches found.")

    with sk3:
        st.markdown("**❌ Missing from Resume**")
        for s in result.get("missing_skills", []):
            st.markdown(
                f"<span style='color:{COLORS['red']}; font-size:13px;'>✗ {s}</span>",
                unsafe_allow_html=True,
            )
        if not result.get("missing_skills"):
            st.success("No critical gaps!", icon="🎉")

    # ── Strengths + Improvements ──────────────────────────────────────────────
    st.markdown("### 💡 AI Feedback")
    f1, f2 = st.columns(2)

    with f1:
        st.markdown("**💪 Strengths**")
        for s in result.get("strengths", []):
            st.markdown(
                f"<div style='background:{COLORS['green']}12; border-left:3px solid {COLORS['green']}; "
                f"padding:8px 12px; border-radius:0 8px 8px 0; margin-bottom:6px; font-size:14px;'>"
                f"{s}</div>",
                unsafe_allow_html=True,
            )

    with f2:
        st.markdown("**🎯 Improvements**")
        for s in result.get("improvements", []):
            st.markdown(
                f"<div style='background:{COLORS['amber']}12; border-left:3px solid {COLORS['amber']}; "
                f"padding:8px 12px; border-radius:0 8px 8px 0; margin-bottom:6px; font-size:14px;'>"
                f"{s}</div>",
                unsafe_allow_html=True,
            )

    # ── Course Recommendations ────────────────────────────────────────────────
    st.markdown("### 🎓 Recommended Courses")
    courses = result.get("course_recommendations", [])
    if courses:
        for i, course in enumerate(courses):
            c = COURSE_COLORS[i % len(COURSE_COLORS)]
            col_num, col_info = st.columns([1, 12])
            with col_num:
                st.markdown(
                    f"<div style='background:{c['bg']}; color:{c['text']}; "
                    f"width:32px; height:32px; border-radius:8px; "
                    f"display:flex; align-items:center; justify-content:center; "
                    f"font-weight:700; font-size:14px; margin-top:4px;'>{i+1}</div>",
                    unsafe_allow_html=True,
                )
            with col_info:
                st.markdown(
                    f"**{course.get('title', 'N/A')}**  \n"
                    f"<span style='color:{c['text']}; font-weight:600; font-size:13px;'>"
                    f"{course.get('platform', '')}</span>"
                    f"<span style='color:#7a7a9a; font-size:13px;'> · {course.get('reason', '')}</span>",
                    unsafe_allow_html=True,
                )
            if i < len(courses) - 1:
                st.markdown(
                    "<hr style='margin:4px 0; border-color:#2a2a3e;'>",
                    unsafe_allow_html=True,
                )
    else:
        st.caption("No course recommendations available.")

    # ── Download report ───────────────────────────────────────────────────────
    st.markdown("### 📥 Export Report")
    _render_download(result)


# ── Download CSV ──────────────────────────────────────────────────────────────
def _render_download(result: dict):
    rows = {
        "Name":              result.get("name", ""),
        "Email":             result.get("email", ""),
        "Phone":             result.get("phone", ""),
        "Experience Level":  result.get("experience_level", ""),
        "Predicted Field":   result.get("predicted_field", ""),
        "Match Score":       result.get("match_score", 0),
        "Extracted Skills":  skill_list_to_csv(result.get("extracted_skills", [])),
        "Matched Skills":    skill_list_to_csv(result.get("matched_skills",   [])),
        "Missing Skills":    skill_list_to_csv(result.get("missing_skills",   [])),
        "Has Objective":     result.get("resume_sections", {}).get("has_objective",      False),
        "Has Education":     result.get("resume_sections", {}).get("has_education",      False),
        "Has Experience":    result.get("resume_sections", {}).get("has_experience",     False),
        "Has Projects":      result.get("resume_sections", {}).get("has_projects",       False),
        "Has Achievements":  result.get("resume_sections", {}).get("has_achievements",   False),
        "Has Certifications":result.get("resume_sections", {}).get("has_certifications", False),
        "Strengths":         " | ".join(result.get("strengths",    [])),
        "Improvements":      " | ".join(result.get("improvements", [])),
        "Overall Summary":   result.get("overall_summary", ""),
    }

    df = pd.DataFrame([rows])
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Full Report as CSV",
        data=csv,
        file_name=f"resume_analysis_{result.get('name', 'report').replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True,
    )