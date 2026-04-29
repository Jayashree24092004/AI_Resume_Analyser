# ─────────────────────────────────────────────────────────────────────────────
# utils/helpers.py  ·  Utility functions: score bands, formatting, session state
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
from constants import SCORE_BANDS, FIELD_COLOR_MAP, COLORS


def get_score_band(score: int) -> dict:
    """Return label, color, and message for a given score."""
    for low, high, label, color, message in SCORE_BANDS:
        if low <= score <= high:
            return {"label": label, "color": color, "message": message}
    return {"label": "Unknown", "color": "gray", "message": ""}


def get_field_color(field: str) -> str:
    """Return hex color for a predicted field."""
    return FIELD_COLOR_MAP.get(field, COLORS["muted"])


def format_file_size(num_bytes: int) -> str:
    """Human-readable file size."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 ** 2):.1f} MB"


def score_color_hex(score: int) -> str:
    """Return a hex color matching the score band."""
    band = get_score_band(score)
    color_map = {
        "green":  COLORS["green"],
        "orange": COLORS["amber"],
        "red":    COLORS["red"],
        "gray":   COLORS["muted"],
    }
    return color_map.get(band["color"], COLORS["muted"])


def init_session_state():
    """Initialise all required Streamlit session state keys."""
    defaults = {
        "result":       None,
        "jd":           "",
        "resume_info":  None,
        "analysing":    False,
        "error":        "",
        "history":      [],   # list of past result dicts
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_analysis():
    """Clear current analysis result and resume, keep JD."""
    st.session_state.result      = None
    st.session_state.resume_info = None
    st.session_state.error       = ""


def save_to_history(result: dict):
    """Append a result snapshot to in-memory history (max 10)."""
    snapshot = {
        "name":            result.get("name", "Unknown"),
        "predicted_field": result.get("predicted_field", ""),
        "match_score":     result.get("match_score", 0),
        "experience_level":result.get("experience_level", ""),
    }
    st.session_state.history.insert(0, snapshot)
    st.session_state.history = st.session_state.history[:10]


def skill_list_to_csv(skills: list[str]) -> str:
    """Convert skill list to comma-separated string."""
    return ", ".join(skills) if skills else "None detected"