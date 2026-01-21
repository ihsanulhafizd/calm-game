import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# CONFIG
# ==================================================
APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"
DAILY_FILE = "daily_journey.csv"

st.set_page_config(
    page_title=APP_TITLE_EN,
    page_icon="💗",
    layout="centered"
)

# ==================================================
# STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def go(p):
    st.session_state.page = p

# ==================================================
# DATE
# ==================================================
now = datetime.now()
weekday = now.strftime("%A")
today_str = now.strftime("%d %B")

# ==================================================
# TEXT
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

BIRTHDAY_EN = "🎉 Happy Birthday, my love.\n\nToday is for you."
BIRTHDAY_ID = "🎉 Selamat ulang tahun, sayang.\n\nHari ini tentang kamu."

TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": "My love,\n\nThis space exists only to stay with you.\n\nI’m here.",
        "start": "Come in",
        "daily": "How does today feel?",
        "msg": BIRTHDAY_EN if today_str == "27 February" else DAILY_EN.get(weekday, ""),
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, write a few words:",
        "save": "Save",
        "thanks": "Thank you for being here.\n\nI’m proud of you."
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": "Sayang,\n\nRuang ini ada untuk menemanimu.\n\nAku di sini.",
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "msg": BIRTHDAY_ID if today_str == "27 February" else DAILY_ID.get(weekday, ""),
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau mau, tuliskan sedikit:",
        "save": "Simpan",
        "thanks": "Terima kasih sudah hadir.\n\nAku bangga padamu."
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE + ANIMATION
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.block-container {
    max-width: 620px;
    padding-top: 1.5rem;
}

.lang {
    font-size: 13px;
    text-align: right;
    margin-bottom: 1rem;
}

.lang span {
    cursor: pointer;
    margin-left: 6px;
}

.active { font-weight: 600; }
.inactive { opacity: 0.45; }

/* Fireflies */
.firefly {
    position: fixed;
    width: 6px;
    height: 6px;
    background: rgba(255,255,255,0.6);
    border-radius: 50%;
    filter: blur(1px);
    animation: float 30s linear infinite;
}

@keyframes float {
    0%   { transform: translate(-10vw, 110vh); opacity: 0; }
    20%  { opacity: 0.6; }
    80%  { opacity: 0.4; }
    100% { transform: translate(110vw, -10vh); opacity: 0; }
}
</style>

<div class="firefly" style="left:20%; animation-duration:26s;"></div>
<div class="firefly" style="left:50%; animation-duration:32s;"></div>
<div class="firefly" style="left:75%; animation-duration:28s;"></div>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (INLINE ONLY)
# ==================================================
_, lang_col = st.columns([4,2])
with lang_col:
    st.markdown(
        f"""
        <div class="lang">
          <span class="{'active' if st.session_state.lang=='en' else 'inactive'}"
                onclick="document.getElementById('btn_en').click()">EN</span> |
          <span class="{'active' if st.session_state.lang=='id' else 'inactive'}"
                onclick="document.getElementById('btn_id').click()">ID</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("EN", key="btn_en", on_click=lambda: st.session_state.update(lang="en"), help="", args=None)
    st.button("ID", key="btn_id", on_click=lambda: st.session_state.update(lang="id"), help="", args=None)

# ==================================================
# DATA
# ==================================================
if not os.path.exists(DAILY_FILE):
    pd.DataFrame(columns=["date","time","choice","note"]).to_csv(DAILY_FILE, index=False)

df = pd.read_csv(DAILY_FILE)

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
    st.markdown(T["msg"])
    choice = st.radio("", T["choices"])
    note = st.text_area(T["note"], height=80)
    if st.button(T["save"]):
        df.loc[len(df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            choice,
            note
        ]
        df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"])
    if st.button("OK"):
        go("landing")
