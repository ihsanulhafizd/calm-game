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
    page_title="🌱 Gentle Living Journey",
    page_icon="🌙",
    layout="centered"
)

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

# ==================================================
# DIALOGUE
# ==================================================
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
    world_text = "🌙 The world feels quiet and safe."
elif total_steps < 50:
    world_anim = world_dawn
    world_text = "🌅 Light is slowly appearing."
else:
    world_anim = world_garden
    world_text = "🌿 The world feels warm and alive."

# ==================================================
# MODE
# ==================================================
mode = st.sidebar.radio("Mode", ["🎮 Journey", "👀 Companion View"])

# ==================================================
# PLAYER MODE
# ==================================================
if mode == "🎮 Journey":
    st.title(f"🌱 Gentle Living Journey with {PLAYER_NAME}")
    st.caption("A calm shared space. Nothing to complete.")

    # 🌫️ VISUAL AMBIENCE FIRST (INI YANG MEMBERI FEEL MALL)
    st.markdown("### 🌫️ Ambient Space")
    st.caption("A quiet public space feeling, like a calm mall or loft.")

    # 🎧 SOUND (STREAMLIT SAFE)
    st.audio(
        "https://cdn.pixabay.com/download/audio/2022/10/30/audio_4f98c8f6bb.mp3?filename=lofi-ambient-121073.mp3",
        format="audio/mp3"
    )
    st.caption("▶️ Tap once to start soft loft ambience.")

    # 🌍 WORLD
    st.markdown("### 🌍 The World")
    st_lottie(world_anim, height=220)
    st.caption(world_text)

    # 🤍 COMPANION
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
    animation = lottie_idle

    if choice == "🌱 Sit together quietly":
        step = 1
        animation = lottie_idle
    elif choice == "🚶 Walk a little":
        step = 2
        animation = lottie_walk
    elif choice == "🌙 Rest and stay still":
        step = 0
        animation = lottie_rest

    st_lottie(animation, height=260)

    if st.button("✨ Stay in this moment"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat(
            [df, pd.DataFrame([[today, step, choice]], columns=["date", "step", "choice"])],
            ignore_index=True
        )
        df.to_csv(DATA_FILE, index=False)

        st.success(random.choice(DIALOGUE))
        st.progress(min((total_steps + step) / 100, 1.0))

    st.info(
        "💬 This space does not ask anything of you.\n\n"
        "💚 You are allowed to simply be here."
    )

# ==================================================
# VIEWER MODE
# ==================================================
if mode == "👀 Companion View":
    st.title("👀 Journey Overview")

    password = st.text_input("Viewer Password", type="password")

    if password != VIEWER_PASSWORD:
        st.warning("Enter the correct password.")
    else:
        st.success("Access granted")

        if not df.empty:
            st.dataframe(df)
            st.metric("Total Gentle Steps", total_steps)
            st.line_chart(df.set_index("date")["step"])
