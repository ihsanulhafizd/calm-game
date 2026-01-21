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
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def go(page):
    st.session_state.page = page

# ==================================================
# DATE
# ==================================================
now = datetime.now()
weekday = now.strftime("%A")
today_str = now.strftime("%d %B")

# ==================================================
# MESSAGES
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
    "Today the world feels brighter because you exist.\n\n"
    "You don’t need to be strong today.\n"
    "Just be.\n\n"
    "You are deeply loved."
)

BIRTHDAY_ID = (
    "🎉 Selamat ulang tahun, sayang.\n\n"
    "Hari ini dunia terasa lebih hangat karena kamu ada.\n\n"
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
# STYLE — FONT + DECORATION
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    letter-spacing: -0.01em;
}

.block-container {
    max-width: 620px;
    padding-top: 1.6rem;
}

/* Language */
.lang {
    text-align: right;
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 1rem;
}

.lang span {
    cursor: pointer;
    margin-left: 6px;
}

.active {
    font-weight: 600;
    color: #111827;
}

.inactive {
    color: #9ca3af;
}

/* Floating stars */
.star {
    position: fixed;
    top: -10px;
    font-size: 10px;
    color: rgba(255,255,255,0.4);
    animation: fall 20s linear infinite;
}

@keyframes fall {
    to {
        transform: translateY(110vh);
    }
}

/* Butterfly */
.butterfly {
    position: fixed;
    left: -50px;
    top: 40%;
    font-size: 18px;
    opacity: 0.15;
    animation: fly 25s linear infinite;
}

@keyframes fly {
    to {
        transform: translateX(120vw);
    }
}

button {
    border-radius: 14px !important;
}
</style>

<div class="star" style="left:10%">✦</div>
<div class="star" style="left:40%">✧</div>
<div class="star" style="left:70%">✦</div>
<div class="butterfly">🦋</div>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH — EN | ID
# ==================================================
_, lang_col = st.columns([4,2])
with lang_col:
    st.markdown(
        f"""
        <div class="lang">
            <span class="{'active' if st.session_state.lang=='en' else 'inactive'}"
                  onclick="document.getElementById('en').click()">EN</span> |
            <span class="{'active' if st.session_state.lang=='id' else 'inactive'}"
                  onclick="document.getElementById('id').click()">ID</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button("EN", key="en", on_click=lambda: st.session_state.update(lang="en"))
    st.button("ID", key="id", on_click=lambda: st.session_state.update(lang="id"))

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
