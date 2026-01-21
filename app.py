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
# TIME LOGIC
# ==================================================
now = datetime.now()
hour = now.hour
weekday = now.strftime("%A")
today_str = now.strftime("%d %B")

def time_phase():
    if 0 <= hour < 6:
        return "deep_night"
    elif 18 <= hour <= 23:
        return "night"
    else:
        return "day"

PHASE = time_phase()

# ==================================================
# BOOK-STYLE MESSAGES (EN)
# ==================================================
EN_MESSAGES = {
    "day": (
        "This page opens gently.\n\n"
        "There is nothing you are expected to do here.\n"
        "Nothing you need to fix.\n"
        "Nothing you need to explain.\n\n"
        "You are allowed to arrive exactly as you are,\n"
        "with whatever thoughts, feelings, or emptiness you carry today.\n\n"
        "This space will not rush you.\n"
        "It will simply sit with you,\n"
        "one page at a time."
    ),
    "night": (
        "The night has settled in.\n\n"
        "If the world feels quieter but your thoughts feel louder,\n"
        "you do not need to fight them here.\n\n"
        "This page is not asking you to solve anything.\n"
        "It is only asking you to soften.\n\n"
        "Lay down what you carried today.\n"
        "You don’t have to hold it alone."
    ),
    "deep_night": (
        "It is very late now.\n\n"
        "The hours are quiet, and it can feel like the world has stepped away.\n"
        "If you are still awake, still thinking, still feeling — that is okay.\n\n"
        "You do not need answers in this darkness.\n"
        "You do not need clarity right now.\n\n"
        "Just breathe.\n"
        "Just stay.\n\n"
        "This page is here with you."
    )
}

# ==================================================
# BOOK-STYLE MESSAGES (ID)
# ==================================================
ID_MESSAGES = {
    "day": (
        "Halaman ini terbuka dengan pelan.\n\n"
        "Tidak ada yang diharapkan darimu di sini.\n"
        "Tidak ada yang perlu kamu perbaiki.\n"
        "Tidak ada yang perlu kamu jelaskan.\n\n"
        "Kamu boleh datang apa adanya,\n"
        "dengan pikiran, perasaan, atau kekosongan apa pun hari ini.\n\n"
        "Ruang ini tidak akan menggesamu.\n"
        "Ia hanya akan duduk bersamamu,\n"
        "halaman demi halaman."
    ),
    "night": (
        "Malam telah tiba.\n\n"
        "Jika dunia terasa lebih sunyi tapi pikiranmu terasa lebih ramai,\n"
        "kamu tidak perlu melawannya di sini.\n\n"
        "Halaman ini tidak meminta kamu menyelesaikan apa pun.\n"
        "Ia hanya mengajakmu melunak.\n\n"
        "Letakkan beban hari ini.\n"
        "Kamu tidak harus menanggungnya sendirian."
    ),
    "deep_night": (
        "Sekarang sudah sangat larut.\n\n"
        "Jam-jam ini sering terasa sepi dan panjang.\n"
        "Jika kamu masih terjaga, masih berpikir, masih merasa,\n"
        "itu tidak apa-apa.\n\n"
        "Kamu tidak membutuhkan jawaban malam ini.\n"
        "Kamu tidak harus mengerti segalanya sekarang.\n\n"
        "Bernapaslah.\n"
        "Tetaplah di sini.\n\n"
        "Halaman ini menemanimu."
    )
}

# 🎉 Birthday override
BIRTHDAY_EN = (
    "🎉 *Happy Birthday, my love.*\n\n"
    "*Today is not a day to carry weight.*\n\n"
    "*Let today hold you instead.*\n\n"
    "*You are deeply loved — exactly as you are.*"
)

BIRTHDAY_ID = (
    "🎉 *Selamat ulang tahun, sayang.*\n\n"
    "*Hari ini bukan hari untuk menanggung beban.*\n\n"
    "*Biarkan hari ini yang memelukmu.*\n\n"
    "*Kamu sangat dicintai — apa adanya.*"
)

# ==================================================
# TEXT MAP
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": BIRTHDAY_EN if today_str == "27 February" else EN_MESSAGES[PHASE],
        "start": "Turn the page",
        "daily": "How does today feel?",
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "You may write anything you want here:",
        "save": "Save",
        "thanks": (
            "*Thank you for opening this page today.*\n\n"
            "*What you shared stays here.*\n\n"
            "*You may rest now.*"
        )
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": BIRTHDAY_ID if today_str == "27 February" else ID_MESSAGES[PHASE],
        "start": "Buka halaman",
        "daily": "Bagaimana hari ini terasa?",
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kamu boleh menuliskan apa pun di sini:",
        "save": "Simpan",
        "thanks": (
            "*Terima kasih sudah membuka halaman ini hari ini.*\n\n"
            "*Apa pun yang kamu tuliskan aman di sini.*\n\n"
            "*Istirahatlah.*"
        )
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (BOOK FEEL)
# ==================================================
st.markdown("""
<style>
.block-container {
    max-width: 640px;
    padding-top: 2rem;
}
p {
    font-style: italic;
    line-height: 1.95;
    font-size: 16px;
}
.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
    opacity: 0.8;
}
.lang span {
    cursor: pointer;
    margin-left: 6px;
}
.active {
    font-weight: 600;
}
.inactive {
    opacity: 0.45;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (VISIBLE)
# ==================================================
st.markdown(
    f"""
    <div class="lang">
      <span class="{'active' if st.session_state.lang=='en' else 'inactive'}"
            onclick="document.getElementById('lang_en').click()">EN</span> |
      <span class="{'active' if st.session_state.lang=='id' else 'inactive'}"
            onclick="document.getElementById('lang_id').click()">ID</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.button("EN", key="lang_en", on_click=lambda: st.session_state.update(lang="en"))
st.button("ID", key="lang_id", on_click=lambda: st.session_state.update(lang="id"))

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
    choice = st.radio("", T["choices"])
    note = st.text_area(T["note"], height=160)
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
    if st.button("Close"):
        go("landing")
