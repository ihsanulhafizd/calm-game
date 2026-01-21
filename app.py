import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests
from streamlit_lottie import st_lottie

# =========================
# CONFIG
# =========================
PLAYER_NAME = "Zara"   # ganti ke "Sayang" jika mau
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

# Companion states (non-human creature)
lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

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
# MODE
# =========================
mode = st.sidebar.radio("Mode", ["🎮 Journey", "👀 Companion View"])

# =========================
# PLAYER MODE
# =========================
if mode == "🎮 Journey":
    st.title(f"🌱 A Gentle Journey with You, {PLAYER_NAME}")
    st.caption("No tasks. No scores. Just gentle presence.")

    st.markdown("### 🤍 Your companion is here")

    choice = st.radio(
        "",
        [
            "🌱 Sit together quietly",
            "🚶 Walk a little",
            "🌙 Rest and stay still"
        ]
    )

    # Default values
    step = 0
    message = ""
    animation = lottie_idle

    if choice == "🌱 Sit together quietly":
        step = 1
        message = "Being here together already matters."
        animation = lottie_idle
    elif choice == "🚶 Walk a little":
        step = 2
        message = "A small movement forward."
        animation = lottie_walk
    elif choice == "🌙 Rest and stay still":
        step = 0
        message = "Resting is allowed. Nothing is lost."
        animation = lottie_rest

    st_lottie(animation, height=260)

    if st.button("✨ Stay in this moment"):
        today = datetime.now().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([[today, step, choice]], columns=["date", "step", "choice"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success(f"I'm here with you, {PLAYER_NAME}.")
        st.caption(message)

        st.markdown("### 🌍 Journey Progress")
        st.progress(min((total_steps + step) / 100, 1.0))
        st.caption(f"The journey has gently moved {total_steps + step} steps.")

    st.markdown("---")
    st.info(
        "💬 This journey does not rush.\n\n"
        "💚 Heavy days do not erase progress.\n\n"
        "🌙 You are not being measured."
    )

# =========================
# VIEWER MODE
# =========================
if mode == "👀 Companion View":
    st.title("👀 Companion Overview")

    password = st.text_input("Viewer Password", type="password")

    if password != VIEWER_PASSWORD:
        st.warning("Enter the correct password.")
    else:
        st.success("Access granted")

        if df.empty:
            st.info("The journey has just begun.")
        else:
            st.dataframe(df)

            st.metric("Total Gentle Steps", total_steps)
            st.line_chart(df.set_index("date")["step"])

        st.caption(
            "This view is for understanding, not control.\n"
            "Presence matters more than speed."
        )
