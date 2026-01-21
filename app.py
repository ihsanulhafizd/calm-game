import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import requests
from streamlit_lottie import st_lottie

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Gentle Living Journey",
    page_icon="🌙",
    layout="centered"
)

# ==================================================
# SOFT UI STYLE (LOFT / GALLERY FEEL)
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f6f7f4;
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 720px;
}
h1, h2, h3 {
    font-weight: 500;
    letter-spacing: 0.2px;
}
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 20px 22px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
}
.caption {
    color: #6b7280;
    font-size: 13px;
}
button[kind="primary"] {
    border-radius: 14px;
    background: #e5e7eb;
    color: #111827;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# CONFIG
# ==================================================
PLAYER_NAME = "Zara"
VIEWER_PASSWORD = "calm123"
DATA_FILE = "journey.csv"

# ==================================================
# LOAD LOTTIE
# ==================================================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Companion
lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

# World
world_night = load_lottie("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
world_dawn = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jmBauI.json")
world_garden = load_lottie("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

# Dialogue
DIALOGUE = [
    "I’m here with you.",
    "There is no rush.",
    "You are allowed to rest.",
    "Quiet moments matter.",
    "Nothing is required of you."
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
    world_anim = world_night
    world_text = "The world feels quiet and safe."
elif total_steps < 50:
    world_anim = world_dawn
    world_text = "Light is slowly appearing."
else:
    world_anim = world_garden
    world_text = "The world feels warm and alive."

# ==================================================
# MODE
# ==================================================
mode = st.sidebar.radio("Mode", ["Journey", "Companion View"])

# ==================================================
# PLAYER MODE
# ==================================================
if mode == "Journey":
    st.markdown(f"<h1>🌱 Gentle Living Journey</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='caption'>A calm space for {PLAYER_NAME}. Nothing to complete.</p>", unsafe_allow_html=True)

    # Ambient
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("🌫️ **Ambient Space**")
    st.audio(
        "https://cdn.pixabay.com/download/audio/2022/10/30/audio_4f98c8f6bb.mp3?filename=lofi-ambient-121073.mp3",
        format="audio/mp3"
    )
    st.markdown("<p class='caption'>Soft background ambience. Tap once to play.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # World
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("🌍 **The World**")
    st_lottie(world_anim, height=200)
    st.markdown(f"<p class='caption'>{world_text}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Companion
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("🤍 **Your Companion**")

    choice = st.radio(
        "",
        ["Sit quietly together", "Walk a little", "Rest and stay still"],
        label_visibility="collapsed"
    )

    step = 0
    animation = lottie_idle

    if choice == "Sit quietly together":
        step = 1
        animation = lottie_idle
    elif choice == "Walk a little":
        step = 2
        animation = lottie_walk
    else:
        step = 0
        animation = lottie_rest

    st_lottie(animation, height=240)

    if st.button("Stay in this moment"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat([df, pd.DataFrame([[today, step, choice]], columns=df.columns)])
        df.to_csv(DATA_FILE, index=False)

        st.success(random.choice(DIALOGUE))
        st.progress(min((total_steps + step) / 100, 1.0))

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# VIEWER MODE
# ==================================================
if mode == "Companion View":
    st.markdown("<h2>👀 Journey Overview</h2>", unsafe_allow_html=True)
    password = st.text_input("Password", type="password")

    if password == VIEWER_PASSWORD:
        st.dataframe(df)
        st.metric("Total Gentle Steps", total_steps)
        st.line_chart(df.set_index("date")["step"])
    else:
        st.warning("Enter correct password.")
