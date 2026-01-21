import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import requests
from streamlit_lottie import st_lottie

# ==================================================
# BASIC CONFIG
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
# SOFT MINIMAL UI STYLE (GALLERY / LOFT)
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f6f7f4;
}
.block-container {
    padding-top: 3rem;
    max-width: 720px;
}
h1, h2 {
    font-weight: 500;
    letter-spacing: 0.3px;
}
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
}
.caption {
    color: #6b7280;
    font-size: 13px;
}
.nav {
    display: flex;
    gap: 12px;
    margin-bottom: 30px;
}
.nav button {
    background: #eef0ec;
    border: none;
    border-radius: 14px;
    padding: 8px 14px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD LOTTIE (ANIMASI HALUS)
# ==================================================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_idle = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_walk = load_lottie("https://assets6.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_rest = load_lottie("https://assets8.lottiefiles.com/packages/lf20_0fhlytwe.json")

world_night = load_lottie("https://assets2.lottiefiles.com/packages/lf20_3rwasyjy.json")
world_dawn = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jmBauI.json")
world_garden = load_lottie("https://assets6.lottiefiles.com/packages/lf20_x62chJ.json")

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
# SESSION PAGE CONTROL
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def go(page):
    st.session_state.page = page

# ==================================================
# LANDING PAGE (OPENING)
# ==================================================
if st.session_state.page == "landing":
    st.markdown("<h1>🌙 Gentle Living Journey</h1>", unsafe_allow_html=True)
    st.markdown("<p class='caption'>A calm space. Nothing to achieve.</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st_lottie(lottie_idle, height=220)
    st.markdown("""
    <p class='caption'>
    This space is not a task.<br>
    It will not measure you.<br>
    You can move slowly — or not at all.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Enter"):
        go("journey")

# ==================================================
# JOURNEY PAGE
# ==================================================
elif st.session_state.page == "journey":
    st.markdown("<h2>🤍 Journey</h2>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        ["Sit quietly", "Walk a little", "Rest"],
        label_visibility="collapsed"
    )

    step = 0
    animation = lottie_idle

    if choice == "Sit quietly":
        step = 1
        animation = lottie_idle
    elif choice == "Walk a little":
        step = 2
        animation = lottie_walk
    else:
        step = 0
        animation = lottie_rest

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st_lottie(animation, height=240)

    if st.button("Stay here"):
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.concat([df, pd.DataFrame([[today, step, choice]], columns=df.columns)])
        df.to_csv(DATA_FILE, index=False)
        st.success(random.choice([
            "I’m here with you.",
            "There is no rush.",
            "Quiet moments matter."
        ]))
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("View the world"):
        go("world")

# ==================================================
# WORLD PAGE
# ==================================================
elif st.session_state.page == "world":
    st.markdown("<h2>🌍 The World</h2>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st_lottie(world_anim, height=220)
    st.markdown(f"<p class='caption'>{world_text}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Back to journey"):
        go("journey")

# ==================================================
# VIEWER PAGE
# ==================================================
elif st.session_state.page == "viewer":
    st.markdown("<h2>👀 Companion View</h2>", unsafe_allow_html=True)
    password = st.text_input("Password", type="password")

    if password == VIEWER_PASSWORD:
        st.dataframe(df)
        st.metric("Total Gentle Steps", total_steps)
    else:
        st.warning("Access restricted.")
