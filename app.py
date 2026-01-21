import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# IDENTITAS
# ==================================================
DISPLAY_NAME = "Zara"
FULL_NAME = "Azzahra Muhabbah Zain"
VIEWER_PASSWORD = "06september2025"

APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"

# ==================================================
# FILES
# ==================================================
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
    st.session_state.lang = "en"   # default English

def go(page):
    st.session_state.page = page

# ==================================================
# TANGGAL HARI INI
# ==================================================
today = datetime.now()
weekday = today.strftime("%A")
today_str = today.strftime("%d %B")

# ==================================================
# PESAN HARIAN
# ==================================================
DAILY_MESSAGES_EN = {
    "Monday": "Take today slowly. I’m right here with you.",
    "Tuesday": "You’re doing enough, even if it doesn’t feel like it.",
    "Wednesday": "Pause when you need to. You’re allowed to.",
    "Thursday": "Not every step needs strength. Presence is enough.",
    "Friday": "You’ve carried a lot this week. Be gentle with yourself.",
    "Saturday": "Rest is not wasted time. It matters.",
    "Sunday": "Whatever tomorrow brings, you won’t face it alone."
}

DAILY_MESSAGES_ID = {
    "Monday": "Jalani hari ini pelan-pelan. Aku ada di sini.",
    "Tuesday": "Apa yang kamu lakukan hari ini sudah cukup.",
    "Wednesday": "Berhenti sejenak tidak apa-apa.",
    "Thursday": "Tidak semua langkah harus kuat.",
    "Friday": "Minggu ini berat. Tolong lembut pada dirimu.",
    "Saturday": "Beristirahat bukan hal sia-sia.",
    "Sunday": "Apa pun besok, kamu tidak sendirian."
}

# 🎉 BIRTHDAY MESSAGE – 27 FEBRUARY
BIRTHDAY_EN = (
    "🎉 Happy Birthday, my love.\n\n"
    "Today is not just another day.\n"
    "It’s the day the world became warmer because you arrived.\n\n"
    "You don’t need to be strong today.\n"
    "You don’t need to carry anything.\n\n"
    "Today, you are celebrated.\n"
    "And I’m endlessly grateful for you."
)

BIRTHDAY_ID = (
    "🎉 Selamat ulang tahun, sayang.\n\n"
    "Hari ini bukan hari biasa.\n"
    "Ini hari ketika dunia menjadi lebih hangat karena kamu ada.\n\n"
    "Hari ini kamu tidak perlu kuat.\n"
    "Tidak perlu menanggung apa pun.\n\n"
    "Hari ini tentang kamu.\n"
    "Dan aku bersyukur kamu ada."
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
        "message": BIRTHDAY_EN if today_str == "27 February" else DAILY_MESSAGES_EN.get(weekday, ""),
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, you can write a few words:",
        "save": "Save",
        "thanks": (
            "Thank you for being here today.\n\n"
            "Whatever you shared is enough.\n"
            "I’m proud of you."
        )
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": (
            "Sayang,\n\n"
            "Ruang ini ada untuk menemanimu.\n"
            "Tanpa tuntutan. Tanpa penilaian.\n\n"
            "Hanya kehadiran.\n\n"
            "Aku di sini."
        ),
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "message": BIRTHDAY_ID if today_str == "27 February" else DAILY_MESSAGES_ID.get(weekday, ""),
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau mau, tuliskan sedikit:",
        "save": "Simpan",
        "thanks": (
            "Terima kasih sudah hadir hari ini.\n\n"
            "Apa pun yang kamu tulis sudah cukup.\n"
            "Aku bangga padamu."
        )
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (MINIMAL)
# ==================================================
st.markdown("""
<style>
.block-container { max-width: 640px; padding-top: 1.2rem; }
p { line-height: 1.6; }
.lang { font-size: 13px; color: #6b7280; text-align: right; }
button { border-radius: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (INLINE)
# ==================================================
left, right = st.columns([4,2])
with right:
    st.markdown("Language:", unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    with l1:
        if st.button("English"):
            st.session_state.lang = "en"
    with l2:
        if st.button("Indonesia"):
            st.session_state.lang = "id"

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
    st.markdown(f"## 💗 {T['title']}")
    st.markdown(T["landing"])
    if st.button(T["start"]):
        go("daily")

elif st.session_state.page == "daily":
    st.markdown(f"### {T['daily']}")
    st.markdown(T["message"])
    choice = st.radio("", T["choices"])
    note = st.text_area(T["note"], height=80)
    if st.button(T["save"]):
        now = datetime.now()
        daily_df.loc[len(daily_df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            choice,
            note
        ]
        daily_df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"])
    if st.button("OK"):
        go("landing")
