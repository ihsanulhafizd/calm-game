import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =========================
# CONFIG
# =========================
PLAYER_NAME = "Zara"     # ganti ke "Sayang" kalau mau
VIEWER_PASSWORD = "calm123"
DATA_FILE = "journey.csv"

st.set_page_config(
    page_title="🌱 A Gentle Journey",
    page_icon="🌙",
    layout="centered"
)

# =========================
# INIT DATA
# =========================
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "step"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

total_steps = df["step"].sum() if not df.empty else 0

# =========================
# MODE SELECT
# =========================
mode = st.sidebar.radio("Mode", ["🎮 Journey", "👀 Companion View"])

# =========================
# PLAYER MODE
# =========================
if mode == "🎮 Journey":
    st.title(f"🌱 A Gentle Journey for {PLAYER_NAME}")
    st.caption("No goals. No pressure. Just moving gently together.")

    st.markdown("### 🌿 Where would you like to be today?")

    choice = st.radio(
        "",
        [
            "🌱 Sit quietly together",
            "🚶 Walk a little",
            "🌤️ Look at the sky",
            "🛌 Rest and stay still"
        ]
    )

    step = 0
    message = ""

    if choice == "🌱 Sit quietly together":
        step = 1
        message = "Being present is already a step."
    elif choice == "🚶 Walk a little":
        step = 2
        message = "A gentle movement forward."
    elif choice == "🌤️ Look at the sky":
        step = 1
        message = "Sometimes looking up is enough."
    elif choice == "🛌 Rest and stay still":
        step = 0
        message = "Resting is not falling behind."

    if st.button("✨ Stay here today"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat(
            [df, pd.DataFrame([[today, step]], columns=["date", "step"])],
            ignore_index=True
        )
        df.to_csv(DATA_FILE, index=False)

        st.success(f"I'm here with you, {PLAYER_NAME}.")
        st.caption(message)

        st.markdown("### 🌍 Journey Progress")
        st.progress(min((total_steps + step) / 100, 1.0))
        st.caption(f"You have gently moved {total_steps + step} steps.")

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
    st.title("👀 Journey Overview")

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
            "This view is for understanding, not controlling.\n"
            "Presence matters more than speed."
        )
