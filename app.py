import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import requests
from streamlit_lottie import st_lottie

# ==================================================
# CONFIGURATION
# ==================================================
PLAYER_NAME = "Zara"              # ganti ke "Sayang" jika mau
VIEWER_PASSWORD = "calm123"       # ganti jika perlu
DATA_FILE = "journey.csv"

st.set_page_config(
    page_title="🌱 A Gentle Living Journey",
    page_icon="🌙",
    layout="centered"
)

# ==================================================
# LOAD LOTTIE ANIMATIONS
# ==================================================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Companion (non-human creature)
lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

# World evolution
world_night = load_lottie("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
world_dawn = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jmBauI.json")
world_garden = load_lottie("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

# ==================================================
# COMPANION DIALOGUE (SOFT, NON-JUDGMENTAL)
# ==================================================
DIALOGUE = [
    "I’m here with you.",
    "There is no rush.",
    "You are allowed to rest.",
    "Quiet moments matter.",
    "We can stay like this.",
    "Nothing is required of you.",
    "You didn’t disappear today.",
    "Just being here is enough."
]

# ==================================================
# DATA INITIALIZATION
# ==================================================
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "step", "choice"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

total_steps = df["step"].sum() if not df.empty else 0

# ==================================================
# WORLD LOGIC
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
# MODE SELECT
# ==================================================
mode = st.sidebar.radio("Mode", ["🎮 Journey", "👀 Companion View"])

# ==================================================
# PLAYER MODE
# ==================================================
if mode == "🎮 Journey":
    st.title(f"🌱 A Gentle Living Journey with {PLAYER_NAME}")
    st.caption("No goals. No pressure. Just a calm shared space.")

    # 🌫️ LOFT / MALL AMBIENCE (AUTOPLAY MUTED)
    st.markdown("### 🌫️ Ambient Space")

    st.markdown(
        """
        <audio autoplay loop muted id="ambientAudio">
            <source src="https://cdn.pixabay.com/download/audio/2022/10/30/audio_4f98c8f6bb.mp3?filename=lofi-ambient-121073.mp3" type="audio/mpeg">
        </audio>

        <script>
        const audio = document.getElementById("ambientAudio");
        audio.volume = 0.12;

        function toggleSound() {
            audio.muted = !audio.muted;
        }
        </script>

        <button onclick="toggleSound()" style="
            padding:10px 18px;
            border-radius:14px;
            border:none;
            background:#eef2f3;
            font-size:14px;
            cursor:pointer;
            margin-top:8px;
            ">
            🔊 Toggle ambient sound
        </button>

        <p style="font-size:12px; color:gray;">
        Soft loft ambience. Starts muted. You can unmute anytime.
        </p>
        """,
        unsafe_allow_html=True
    )

    # 🌍 WORLD VIEW
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

    # ✨ SAVE MOMENT
    if st.button("✨ Stay in this moment"):
        today = datetime.now().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([[today, step, choice]], columns=["date", "step", "choice"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success(random.choice(DIALOGUE))
        st.progress(min((total_steps + step) / 100, 1.0))

    st.markdown("---")
    st.info(
        "💬 This world does not collapse.\n\n"
        "💚 You are not being tested.\n\n"
        "🌙 You are allowed to exist here."
    )

# ==================================================
# VIEWER MODE (SAFE MONITORING)
# ==================================================
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
            "This view exists for care, not control.\n"
            "Presence matters more than speed."
        )
