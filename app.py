import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ==================================================
# CONFIG
# ==================================================
PLAYER_NAME = "Zara"
VIEWER_PASSWORD = "calm123"

DAILY_FILE = "daily_journey.csv"
WEEKLY_FILE = "weekly_reflection.csv"
PDF_FILE = "zara_progress.pdf"

st.set_page_config(
    page_title="Zara’s Gentle Space",
    page_icon="🌤️",
    layout="centered"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "id"
if "read" not in st.session_state:
    st.session_state.read = False

def go(page):
    st.session_state.page = page

# ==================================================
# LANGUAGE TEXT
# ==================================================
TEXT = {
    "id": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "Sayang,\n\n"
            "Tidak ada yang perlu kamu buktikan hari ini.\n"
            "Tidak ada target, tidak ada tuntutan.\n\n"
            "Tempat ini dibuat untuk menemanimu,\n"
            "bukan untuk menilaimu.\n\n"
            "Tarik napas pelan.\n"
            "Kamu aman di sini."
        ),
        "read": "Aku sudah membaca dan memahami pesan ini",
        "start": "Awal",
        "question": "Hari ini terasa seperti apa?",
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini berat, aku beristirahat"
        ],
        "note": "Kalau kamu mau, ceritakan sedikit alasannya:",
        "save": "Simpan hari ini",
        "thank_title": "Terima kasih, Zara",
        "thank_text": (
            "Terima kasih sudah berhenti sejenak hari ini.\n\n"
            "Apa pun pilihanmu, itu bukan tanda kegagalan.\n"
            "Itu adalah bentuk kejujuran dan keberanian.\n\n"
            "Kamu tidak perlu berubah dengan cepat.\n"
            "Kamu hanya perlu terus ada.\n\n"
            "Tempat ini akan menunggumu,\n"
            "besok, atau kapan pun kamu siap."
        ),
        "back": "Kembali Besok",
        "weekly_title": "Refleksi Mingguan",
        "weekly_locked": "Bagian ini akan terbuka dengan sendirinya setelah beberapa hari.",
        "weekly_q1": "Apa yang terasa paling berat minggu ini?",
        "weekly_q2": "Apa yang sedikit membantu?",
        "weekly_q3": "Apa yang ingin kamu bawa ke minggu depan?",
        "weekly_save": "Simpan refleksi",
        "viewer_title": "Mode Pemantau (Pribadi)",
        "password": "Password",
        "export": "Export PDF"
    },
    "en": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "My love,\n\n"
            "There is nothing you need to prove today.\n"
            "No targets. No expectations.\n\n"
            "This space exists to stay with you,\n"
            "not to judge you.\n\n"
            "Take a slow breath.\n"
            "You are safe here."
        ),
        "read": "I have read and understood this message",
        "start": "Begin",
        "question": "How did today feel?",
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, you can share a little why:",
        "save": "Save today",
        "thank_title": "Thank you, Zara",
        "thank_text": (
            "Thank you for pausing today.\n\n"
            "Whatever you chose, it is not a failure.\n"
            "It is honesty, and that takes courage.\n\n"
            "You don’t need to change quickly.\n"
            "You only need to keep showing up.\n\n"
            "This space will wait for you,\n"
            "tomorrow, or whenever you’re ready."
        ),
        "back": "Come back tomorrow",
        "weekly_title": "Weekly Reflection",
        "weekly_locked": "This space will open gently after a few days.",
        "weekly_q1": "What felt heaviest this week?",
        "weekly_q2": "What helped, even a little?",
        "weekly_q3": "What would you like to carry into next week?",
        "weekly_save": "Save reflection",
        "viewer_title": "Private Observer Mode",
        "password": "Password",
        "export": "Export PDF"
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (NO SCROLL, CLEAN)
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #fbfcfa;
    color: #1f2937;
    font-family: Inter, sans-serif;
}
.block-container {
    max-width: 720px;
    padding-top: 2.5rem;
}
.caption {
    color: #6b7280;
    font-size: 15px;
    line-height: 1.8;
}
button {
    border-radius: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA INIT
# ==================================================
if not os.path.exists(DAILY_FILE):
    pd.DataFrame(columns=["date", "choice", "note", "score"]).to_csv(DAILY_FILE, index=False)
if not os.path.exists(WEEKLY_FILE):
    pd.DataFrame(columns=["week_start", "heavy", "helped", "carry"]).to_csv(WEEKLY_FILE, index=False)

daily_df = pd.read_csv(DAILY_FILE)
weekly_df = pd.read_csv(WEEKLY_FILE)

# ==================================================
# WEEKLY AVAILABILITY
# ==================================================
weekly_available = False
if not daily_df.empty:
    first_day = pd.to_datetime(daily_df["date"]).min()
    if (datetime.now() - first_day).days >= 7:
        weekly_available = True

# ==================================================
# LANGUAGE TOGGLE
# ==================================================
c1, c2 = st.columns(2)
with c1:
    if st.button("🇮🇩"):
        st.session_state.lang = "id"
with c2:
    if st.button("🇺🇸"):
        st.session_state.lang = "en"

# ==================================================
# VIEWER MODE (PRIVATE URL)
# ==================================================
viewer_mode = st.query_params.get("viewer") == "true"

if viewer_mode:
    st.markdown(f"## {T['viewer_title']}")
    password = st.text_input(T["password"], type="password")

    if password == VIEWER_PASSWORD:
        st.dataframe(daily_df)
        st.dataframe(weekly_df)

        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(daily_df["date"]), daily_df["score"], marker="o")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        if st.button(T["export"]):
            fig_path = "progress.png"
            fig.savefig(fig_path)
            doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [Paragraph("Zara’s Private Report", styles["Title"]), Spacer(1, 12), Image(fig_path, 400, 200)]
            doc.build(story)
            st.download_button("⬇️ Download PDF", open(PDF_FILE, "rb"), file_name=PDF_FILE)

# ==================================================
# PLAYER FLOW
# ==================================================
else:
    if st.session_state.page == "landing":
        st.markdown(f"## 🌤️ {T['title']}")
        st.markdown(f"<p class='caption'>{T['landing']}</p>", unsafe_allow_html=True)
        st.checkbox(T["read"], key="read")
        if st.session_state.read and st.button(T["start"]):
            go("daily")

    elif st.session_state.page == "daily":
        st.markdown(f"## 🤍 {T['question']}")
        choice = st.radio("", T["choices"])
        note = st.text_area(T["note"], height=120)
        if st.button(T["save"]):
            today = datetime.now().strftime("%Y-%m-%d")
            score = T["choices"].index(choice)
            daily_df.loc[len(daily_df)] = [today, choice, note, score]
            daily_df.to_csv(DAILY_FILE, index=False)
            go("thanks")

    elif st.session_state.page == "thanks":
        st.markdown(f"## {T['thank_title']}")
        st.markdown(f"<p class='caption'>{T['thank_text']}</p>", unsafe_allow_html=True)
        if st.button(T["back"]):
            go("landing")
