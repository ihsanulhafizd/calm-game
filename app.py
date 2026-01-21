import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import requests
from streamlit_lottie import st_lottie

# ==================================================
# CONFIG
# ==================================================
PLAYER_NAME = "Zara"
VIEWER_PASSWORD = "calm123"
DATA_FILE = "journey.csv"

st.set_page_config(
    page_title="Gentle Living Journey",
    page_icon="🌙",
    layout="centered"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def go(page):
    st.session_state.page = page

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ==================================================
# THEME STYLE
# ==================================================
if st.session_state.theme == "light":
    BG = "#f6f7f4"
    CARD = "#ffffff"
    TEXT = "#1f2937"
    SUB = "#6b7280"
else:
    BG = "#0f1115"
    CARD = "#1a1d24"
    TEXT = "#e5e7eb"
    SUB = "#9ca3af"

st.markdown(f"""
<style>
html, body, [class*="css"] {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Inter', sans-serif;
}}
.block-container {{
    max-width: 720px;
    padding-top: 2.5rem;
}}
.card {{
    background: {CARD};
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    animation: fadeIn 0.7s ease;
}}
.caption {{
    color: {SUB};
    font-size: 13px;
    line-height: 1.6;
}}
button {{
    border-radius: 14px !important;
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD LOTTIE
# ==================================================
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Companion animations
lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

# World animations
world_night = load_lottie("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
world_dawn = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jmBauI.json")
world_garden = load_lottie("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

DIALOGUE = [
    "I’m here with you.",
    "There is no rush.",
    "Quiet moments are enough.",
    "Nothing is required of you.",
    "You are allowed to rest."
]

# ==================================================
# DATA
# ==================================================
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "step", "choice"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

total_steps = df["step"].sum() if not df.empty else 0

# ==================================================
# WORLD STATE
# ==================================================
if total_steps < 20:
    world_anim, world_text = world_night, "The world is quiet and safe."
elif total_steps < 50:
    world_anim, world_text = world_dawn, "Light is slowly appearing."
else:
    world_anim, world_text = world_garden, "The world feels warm and alive."

# ==================================================
# TOP NAV BAR
# ==================================================
nav1, nav2, nav3, nav4 = st.columns([2,2,2,1])

with nav1:
    if st.button("🌱 Journey"):
        go("journey")

with nav2:
    if st.button("🌍 World"):
        go("world")

with nav3:
    if st.button("👀 Viewer"):
        go("viewer")

with nav4:
    if st.button("🌓"):
        toggle_theme()

# ==================================================
# LANDING PAGE
# ==================================================
if st.session_state.page == "landing":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h1>🌙 Gentle Living Journey</h1>", unsafe_allow_html=True)
    st.markdown("<p class='caption'>A calm space. Nothing to achieve.</p>", unsafe_allow_html=True)
    st_lottie(lottie_idle, height=220)
    st.markdown("""
    <p class='caption'>
    This space will not test you.<br>
    You can move slowly — or stay still.
    </p>
    """, unsafe_allow_html=True)
    if st.button("Enter"):
        go("journey")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# JOURNEY PAGE (PLAYER)
# ==================================================
elif st.session_state.page == "journey":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>🤍 Journey</h2>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        ["Sit quietly", "Walk a little", "Rest"],
        label_visibility="collapsed"
    )

    if choice == "Sit quietly":
        step, anim = 1, lottie_idle
    elif choice == "Walk a little":
        step, anim = 2, lottie_walk
    else:
        step, anim = 0, lottie_rest

    st_lottie(anim, height=240)

    if st.button("Stay here"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat(
            [df, pd.DataFrame([[today, step, choice]], columns=df.columns)],
            ignore_index=True
        )
        df.to_csv(DATA_FILE, index=False)
        st.success(random.choice(DIALOGUE))

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# WORLD PAGE
# ==================================================
elif st.session_state.page == "world":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>🌍 The World</h2>", unsafe_allow_html=True)
    st_lottie(world_anim, height=220)
    st.markdown(f"<p class='caption'>{world_text}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# VIEWER PAGE
# ==================================================
elif st.session_state.page == "viewer":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>👀 Companion View</h2>", unsafe_allow_html=True)
    password = st.text_input("Password", type="password")

    if password == VIEWER_PASSWORD:
        st.dataframe(df)
        st.metric("Total Gentle Steps", total_steps)
        st.line_chart(df.set_index("date")["step"])
    else:
        st.warning("Access restricted.")
    st.markdown("</div>", unsafe_allow_html=True)
