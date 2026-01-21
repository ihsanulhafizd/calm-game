import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# IDENTITAS
# ==================================================
FULL_NAME = "Azzahra Muhabbah Zain"
VIEWER_PASSWORD = "06september2025"

APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"

DAILY_FILE = "daily_journey.csv"

st.set_page_config(
    page_title=APP_TITLE_EN,
    page_icon="💗",
    layout="centered"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"  # default English

def go(page):
    st.session_state.page = page

# ==================================================
# HELPER: PAGE COLOR
# ==================================================
def set_bg(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# DATE & DAY
# ==================================================
now = datetime.now()
weekday = now.strftime("%A")
today_str = now.strftime("%d %B")

# ==================================================
# DAILY & BIRTHDAY MESSAGES
# ==================================================
DAILY_EN = {
    "Monday": "Take today slowly. I’m right here with you.",
    "Tuesday": "You are doing enough, even on quiet days.",
    "Wednesday": "Pause when you need to. You’re allowed to.",
    "Thursday": "You don’t need strength for every step.",
    "Friday": "This week asked a lot of you. Be kind to yourself.",
    "Saturday": "Rest is meaningful. It matters.",
    "Sunday": "Whatever tomorrow brings, you won’t face it alone."
}

DAILY_ID = {
    "Monday": "Jalani hari ini pelan-pelan. Aku ada di sini.",
    "Tuesday": "Apa yang kamu lakukan hari ini sudah cukup.",
    "Wednesday": "Berhenti sejenak tidak apa-apa.",
    "Thursday": "Tidak semua langkah harus kuat.",
    "Friday": "Minggu ini berat. Bersikaplah lembut pada dirimu.",
    "Saturday": "Beristirahat itu bermakna.",
    "Sunday": "Apa pun besok, kamu tidak sendirian."
}

BIRTHDAY_EN = (
    "🎉 Happy Birthday, my love.\n\n"
    "Today the world is brighter because you exist.\n\n"
    "You don’t need to be strong today.\n"
    "Just be.\n\n"
    "You are deeply loved."
)

BIRTHDAY_ID = (
    "🎉 Selamat ulang tahun, sayang.\n\n"
    "Hari ini dunia lebih hangat karena kamu ada.\n\n"
    "Hari ini kamu tidak perlu kuat.\n"
    "Cukup jadi dirimu.\n\n"
    "Kamu sangat dicintai."
)

# ==================================================
# TEXT
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": (
            "My love,\n\n"
            "This space exists only to stay with you.\n"
            "No fixing. No proving.\n\n"
            "Just presence.\n\n"
            "I’m here."
        ),
        "start": "Come in",
        "daily": "How does today feel?",
        "message": BIRTHDAY_EN if today_str == "27 February" else DAILY_EN.get(weekday, ""),
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, write a few words:",
        "save": "Save",
        "thanks": "Thank you for being here today.\n\nI’m proud of you."
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": (
            "Sayang,\n\n"
            "Ruang ini ada untuk menemanimu.\n"
            "Tanpa tuntutan.\n\n"
            "Hanya kehadiran.\n\n"
            "Aku di sini."
        ),
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "message": BIRTHDAY_ID if today_str == "27 February" else DAILY_ID.get(weekday, ""),
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau mau, tuliskan sedikit:",
        "save": "Simpan",
        "thanks": "Terima kasih sudah hadir hari ini.\n\nAku bangga padamu."
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (MINIMAL)
# ==================================================
st.markdown("""
<style>
.block-container { max-width: 620px; padding-top: 1.4rem; }
p { line-height: 1.6; }
.lang { font-size: 13px; text-align: right; }
.lang span { cursor: pointer; margin-left: 6px; }
.active { font-weight: 600; color: #111827; }
.inactive { color: #9ca3af; }
button { border-radius: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (ELEGANT INLINE)
# ==================================================
_, lang_col = st.columns([4,2])
with lang_col:
    st.markdown(
        f"""
        <div class="lang">
        Language:
        <span class="{'active' if st.session_state.lang=='en' else 'inactive'}"
              onclick="window.location.hash='en'">English</span> |
        <span class="{'active' if st.session_state.lang=='id' else 'inactive'}"
              onclick="window.location.hash='id'">Indonesia</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Streamlit-safe language change
if st.session_state.get("lang_change"):
    st.session_state.lang = st.session_state.lang_change

# ==================================================
# DATA INIT
# ==================================================
if not os.path.exists(DAILY_FILE):
    pd.DataFrame(columns=["date","time","choice","note"]).to_csv(DAILY_FILE, index=False)

daily_df = pd.read_csv(DAILY_FILE)

# ==================================================
# FLOW
# ==================================================
if st.session_state.page == "landing":
    set_bg("#fefcf8")  # cream
    st.markdown(f"## 💗 {T['title']}")
    st.markdown(T["landing"])
    if st.button(T["start"]):
        go("daily")

elif st.session_state.page == "daily":
    set_bg("#fff7ed")  # soft peach
    st.markdown(f"### {T['daily']}")
    st.markdown(T["message"])
    choice = st.radio("", T["choices"])
    note = st.text_area(T["note"], height=80)
    if st.button(T["save"]):
        daily_df.loc[len(daily_df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            choice,
            note
        ]
        daily_df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    set_bg("#fff1f2")  # soft pink
    st.markdown(T["thanks"])
    if st.button("OK"):
        go("landing")
