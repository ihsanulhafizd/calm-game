import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests
from streamlit_lottie import st_lottie

# =========================
# CONFIG
# =========================
PLAYER_NAME = "Zara"
VIEWER_PASSWORD = "calm123"
DATA_FILE = "journey.csv"

st.set_page_config(
    page_title="🌱 Gentle Companion Journey",
    page_icon="🌙",
    layout="centered"
)

# =========================
# LOAD LOTTIE
# =========================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Companion
lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

# World states
world_night = load_lottie("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
world_dawn = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jmBauI.json")
world_garden = load_lottie("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

# =========================
# INIT DATA
# =========================
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "step", "choice"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

total_steps = df["step"].sum() if not df.empty else 0

# =========================
# WORLD LOGIC
# =========================
if total_steps < 20:
    world_state = "night"
    world_anim = world_night
    world_text = "🌙 The world is quiet and safe."
elif total_steps < 50:
    world_state = "dawn"
    world_anim = world_dawn
    world_text = "🌅 Light is slowly appearing."
else:
    world_state = "garden"
    world_anim = world_garden
    world_text = "🌿 The world is alive and growing."

# =========================
# MODE
# =========================
mode = st.sidebar.radio("Mode", ["🎮 Journey", "👀 Companion View"])

# =========================
# PLAYER MODE
# =========================
if mode == "🎮 Journey":
    st.title(f"🌱 A Gentle Journey with {PLAYER_NAME}")
    st.caption("The world grows with you. No rush.")

    st.markdown("### 🌍 World")
    st_lottie(world_anim, height=220)
    st.caption(world_text)

    st.markdown("### 🤍 Your Companion")

    choice = st.radio(
        "",
        [
            "🌱 Sit together quietly",
            "🚶 Walk a little",
            "🌙 Rest and stay still"
        ]
    )

    step = 0
    message = ""
    animation = lottie_idle

    if choice == "🌱 Sit together quietly":
        step = 1
        message = "Being present is enough."
        animation = lottie_idle
    elif choice == "🚶 Walk a little":
        step = 2
        message = "A gentle step forward."
        animation = lottie_walk
    elif choice == "🌙 Rest and stay still":
        step = 0
        message = "Resting is part of the journey."
        animation = lottie_rest

    st_lottie(animation, height=260)

    if st.button("✨ Stay in this moment"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat(
            [df, pd.DataFrame([[today, step, choice]], columns=["date", "step", "choice"])],
            ignore_index=True
        )
        df.to_csv(DATA_FILE, index=False)

        st.success(f"I'm here with you, {PLAYER_NAME}.")
        st.caption(message)

        st.markdown("### 🌱 Journey Progress")
        st.progress(min((total_steps + step) / 100, 1.0))
        st.caption("Progress continues, even slowly.")

    st.markdown("---")
    st.info(
        "💬 The world never breaks.\n\n"
        "💚 Heavy days do not undo growth.\n\n"
        "🌙 You are safe here."
    )

# =========================
# VIEWER
