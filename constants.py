# ─────────────────────────────────────────────────────────────────────────────
# constants.py  ·  All static data: colors, fields, keywords, courses
# ─────────────────────────────────────────────────────────────────────────────

# ── UI Theme Colors ───────────────────────────────────────────────────────────
COLORS = {
    "accent":       "#6c63ff",
    "teal":         "#00cec9",
    "green":        "#00b894",
    "amber":        "#fdcb6e",
    "red":          "#e17055",
    "pink":         "#fd79a8",
    "blue":         "#74b9ff",
    "muted":        "#7a7a9a",
    "white":        "#ffffff",
    "bg":           "#0a0a0f",
    "card":         "#1a1a26",
}

# ── Field → UI color mapping ──────────────────────────────────────────────────
FIELD_COLOR_MAP = {
    "Data Science":         COLORS["accent"],
    "Web Development":      COLORS["teal"],
    "Android Development":  COLORS["green"],
    "iOS Development":      COLORS["amber"],
    "UI/UX Design":         COLORS["pink"],
    "Software Engineering": COLORS["blue"],
    "DevOps":               COLORS["red"],
    "Cybersecurity":        COLORS["red"],
    "General":              COLORS["muted"],
}

# ── Experience level ordering ─────────────────────────────────────────────────
EXPERIENCE_LEVELS = ["Fresher", "Junior", "Mid-Level", "Senior", "Expert"]

# ── Predicted field choices (sent to Claude) ──────────────────────────────────
PREDICTED_FIELDS = [
    "Data Science",
    "Web Development",
    "Android Development",
    "iOS Development",
    "UI/UX Design",
    "Software Engineering",
    "DevOps",
    "Cybersecurity",
    "General",
]

# ── Resume section names for display ─────────────────────────────────────────
RESUME_SECTIONS = {
    "has_objective":      "Objective / Summary",
    "has_education":      "Education",
    "has_experience":     "Work Experience",
    "has_projects":       "Projects",
    "has_achievements":   "Achievements",
    "has_certifications": "Certifications",
}

# ── Score band thresholds ─────────────────────────────────────────────────────
SCORE_BANDS = [
    (75, 100, "🟢 Strong Match",   "green",  "Great fit — your profile aligns well with this role."),
    (45,  74, "🟡 Moderate Match", "orange", "Decent match — some gaps worth addressing before applying."),
    (0,   44, "🔴 Low Match",      "red",    "Significant gaps detected — consider upskilling first."),
]

# ── Streamlit page config ─────────────────────────────────────────────────────
PAGE_CONFIG = {
    "page_title": "AI Resume Analyser",
    "page_icon":  "🎯",
    "layout":     "wide",
    "initial_sidebar_state": "expanded",
}

# ── Accepted file types ───────────────────────────────────────────────────────
ACCEPTED_FILE_TYPES = ["pdf", "txt", "docx"]

# ── Claude model ──────────────────────────────────────────────────────────────
GEMINI_MODEL      = "gemini-1.5-flash"   # free, fast, great for JSON tasks
GEMINI_MAX_TOKENS = 2000

# ── Job description presets (for demo / quick testing) ───────────────────────
JD_PRESETS = {
    "— Select a preset JD —": "",
    "Data Scientist": """Seeking a skilled Data Scientist with expertise in machine learning,
statistical analysis, and data visualization. Proficiency in Python, R, SQL and experience
with ML frameworks (scikit-learn, TensorFlow, PyTorch) is required. Experience with
pandas, NumPy, Matplotlib, Seaborn, and cloud platforms (AWS/GCP) is a plus.""",

    "Full Stack Developer": """Looking for a Full Stack Developer with strong knowledge of
front-end and back-end technologies. Experience in React, Node.js, Express, REST APIs,
and familiarity with database systems (PostgreSQL, MongoDB) is essential. Knowledge of
Docker, Git, and CI/CD pipelines preferred.""",

    "UI/UX Designer": """We are hiring a creative UX/UI Designer with a passion for creating
intuitive and visually appealing user interfaces. Proficiency in Figma, Adobe XD, and
experience with user research, wireframing, and prototyping is required. Knowledge of
HTML, CSS is a plus.""",

    "Android Developer": """Seeking an Android Developer with proficiency in Kotlin and Java.
Experience with Android SDK, Jetpack Compose, MVVM architecture, Retrofit, Room, and
Google Play deployment. Knowledge of Flutter is a bonus.""",

    "DevOps Engineer": """Looking for a DevOps Engineer experienced in CI/CD pipelines,
Docker, Kubernetes, Terraform, and cloud platforms (AWS, Azure, GCP). Strong scripting
skills in Python or Bash. Experience with monitoring tools like Prometheus and Grafana.""",
}

# ── Course badge colour cycle (used in results_panel) ────────────────────────
COURSE_COLORS = [
    {"bg": "#6c63ff33", "text": "#a29bfe"},
    {"bg": "#00cec933", "text": "#00cec9"},
    {"bg": "#00b89433", "text": "#00b894"},
    {"bg": "#fdcb6e33", "text": "#fdcb6e"},
    {"bg": "#e1705533", "text": "#e17055"},
]