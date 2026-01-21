import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ==================================================
# IDENTITAS
# ==================================================
DISPLAY_NAME = "Zara"
FULL_NAME = "Azzahra Muhabbah Zain"
VIEWER_PASSWORD = "06september2025"
VIEWER_NAME = "Owner"

APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"

# ==================================================
# FILES
# ==================================================
DAILY_FILE = "daily_journey.csv"
VIEWER_LOG_FILE = "viewer_log.csv"
PDF_FILE = "zara_progress.pdf"

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
    st.session_state.lang = "en"   # DEFAULT ENGLISH

def go(page):
    st.session_state.page = page

# ==================================================
# DAILY MESSAGE BY DAY
# ==================================================
DAILY_MESSAGES_EN = {
    "Monday": "Take this day slowly. You don’t have to carry everything at once.",
    "Tuesday": "You’re doing enough, even on days that feel uncertain.",
    "Wednesday": "Pause when you need to. I’m still here with you.",
    "Thursday": "Not every step has to be strong. Gentle steps count too.",
    "Friday": "You’ve carried a lot this week. Be kind to yourself.",
    "Saturday": "Today doesn’t need a purpose. Rest is enough.",
    "Sunday": "Whatever tomorrow brings, you don’t face it alone."
}

DAILY_MESSAGES_ID = {
    "Monday": "Jalani hari ini pelan-pelan. Kamu tidak harus menanggung semuanya.",
    "Tuesday": "Apa yang kamu lakukan hari ini sudah cukup.",
    "Wednesday": "Berhentilah sejenak jika perlu. Aku tetap di sini.",
    "Thursday": "Tidak semua langkah harus kuat. Langkah pelan pun berarti.",
    "Friday": "Minggu ini berat. Tolong bersikap lembut pada dirimu.",
    "Saturday": "Hari ini tidak perlu tujuan. Beristirahat sudah cukup.",
    "Sunday": "Apa pun yang datang besok, kamu tidak sendirian."
}

today_name = datetime.now().strftime("%A")

# ==================================================
# TEXT
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": (
            "My love,\n\n"
            "This space exists for one reason only:\n"
            "to stay with you.\n\n"
            "There is nothing you need to fix today.\n"
            "Nothing you need to prove.\n\n"
            "I’m here. Always."
        ),
        "start": "Come in slowly",
        "daily": "How does today feel, my love?",
        "daily_message": DAILY_MESSAGES_EN.get(today_name, ""),
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, you can share a little why:",
        "save": "Save today",
        "thanks_title": "Thank you, my love",
        "thanks_text": (
            "Thank you for showing up today.\n\n"
            "Whatever you chose,\n"
            "it is not a failure.\n\n"
            "It’s honesty.\n"
            "And that matters.\n\n"
            "Rest now.\n"
            "I’m still here."
        ),
        "next_title": "What Comes Next",
        "next_text": (
            "You don’t need to do anything right now.\n\n"
            "If you want, you can:\n"
            "• rest for a moment\n"
            "• drink some water\n"
            "• take a slow breath\n\n"
            "This space will wait for you."
        ),
        "back": "Back",
        "viewer_title": "Private Observer Mode",
        "password": "Password"
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": (
            "Sayang,\n\n"
            "Ruang ini ada hanya untuk satu hal:\n"
            "menemanimu.\n\n"
            "Tidak ada yang perlu kamu perbaiki hari ini.\n"
            "Tidak ada yang perlu kamu buktikan.\n\n"
            "Aku di sini. Selalu."
        ),
        "start": "Masuk pelan-pelan",
        "daily": "Bagaimana hari ini terasa, sayang?",
        "daily_message": DAILY_MESSAGES_ID.get(today_name, ""),
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau kamu ingin, ceritakan sedikit alasannya:",
        "save": "Simpan hari ini",
        "thanks_title": "Terima kasih, sayang",
        "thanks_text": (
            "Terima kasih sudah hadir hari ini.\n\n"
            "Apa pun pilihanmu,\n"
            "itu bukan kegagalan.\n\n"
            "Itu kejujuran.\n"
            "Dan itu berarti.\n\n"
            "Istirahatlah.\n"
            "Aku tetap di sini."
        ),
        "next_title": "Langkah Selanjutnya",
        "next_text": (
            "Sekarang kamu tidak perlu melakukan apa pun.\n\n"
            "Kalau mau, kamu bisa:\n"
            "• beristirahat sebentar\n"
            "• minum air putih\n"
            "• menarik napas pelan\n\n"
            "Ruang ini akan menunggumu."
        ),
        "back": "Kembali",
        "viewer_title": "Mode Pemantau (Pribadi)",
        "password": "Password"
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE
# ==================================================
st.markdown("""
<style>
.block-container { max-width: 680px; padding-top: 1.5rem; }
.caption { color:#6b7280; font-size:14.5px; line-height:1.6; }
.lang { text-align:right; font-size:13px; color:#6b7280; }
button { border-radius:18px !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (IN PLACE)
# ==================================================
_, right = st.columns([5,1])
with right:
    st.markdown("<div class='lang'>Language</div>", unsafe_allow_html=True)
    if st.button("English"):
        st.session_state.lang = "en"
    if st.button("Indonesia"):
        st.session_state.lang = "id"

# ==================================================
# DATA INIT
# ==================================================
if not os.path.exists(DAILY_FILE):
    pd.DataFrame(columns=["date","time","choice","note"]).to_csv(DAILY_FILE, index=False)
if not os.path.exists(VIEWER_LOG_FILE):
    pd.DataFrame(columns=["date","time","viewer"]).to_csv(VIEWER_LOG_FILE, index=False)

daily_df = pd.read_csv(DAILY_FILE)
viewer_log_df = pd.read_csv(VIEWER_LOG_FILE)

# ==================================================
# VIEWER MODE
# ==================================================
if st.query_params.get("viewer") == "true":
    st.markdown(f"## {T['viewer_title']}")
    st.markdown(f"**Name:** {FULL_NAME}")
    pw = st.text_input(T["password"], type="password")

    if pw == VIEWER_PASSWORD:
        now = datetime.now()
        viewer_log_df.loc[len(viewer_log_df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            VIEWER_NAME
        ]
        viewer_log_df.to_csv(VIEWER_LOG_FILE, index=False)

        st.subheader("Viewer Access Log")
        st.dataframe(viewer_log_df)

        st.subheader("Zara’s Daily Entries")
        st.dataframe(daily_df)

# ==================================================
# PLAYER FLOW
# ==================================================
else:
    if st.session_state.page == "landing":
        st.markdown(f"## 💗 {T['title']}")
        st.markdown(f"<p class='caption'>{T['landing']}</p>", unsafe_allow_html=True)
        if st.button(T["start"]):
            go("daily")

    elif st.session_state.page == "daily":
        st.markdown(f"## 🤍 {T['daily']}")
        st.markdown(f"<p class='caption'>{T['daily_message']}</p>", unsafe_allow_html=True)
        choice = st.radio("", T["choices"])
        note = st.text_area(T["note"], height=90)
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
        st.markdown(f"## {T['thanks_title']}")
        st.markdown(f"<p class='caption'>{T['thanks_text']}</p>", unsafe_allow_html=True)
        if st.button("Continue"):
            go("next")

    elif st.session_state.page == "next":
        st.markdown(f"## {T['next_title']}")
        st.markdown(f"<p class='caption'>{T['next_text']}</p>", unsafe_allow_html=True)
        if st.button(T["back"]):
            go("landing")
