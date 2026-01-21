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
# LANGUAGE SYSTEM
# ==================================================
if "lang" not in st.session_state:
    st.session_state.lang = "id"

TEXT = {
    "id": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "Sayang,\n\n"
            "Kamu tidak perlu menjadi lebih kuat hari ini.\n"
            "Kamu tidak perlu menjelaskan apa pun dengan sempurna.\n\n"
            "Tempat ini tidak menilaimu.\n"
            "Ia hanya menemanimu — pelan dan sabar."
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
        "thanks": "Terima kasih sudah jujur dengan dirimu sendiri, sayang.",
        "weekly": "Refleksi Mingguan",
        "weekly_locked": "Bagian ini akan terbuka setelah beberapa hari.",
        "viewer": "Mode Pemantau (Pribadi)",
        "password": "Password",
        "export": "Export PDF"
    },
    "en": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "My love,\n\n"
            "You don’t need to be stronger today.\n"
            "You don’t need perfect explanations.\n\n"
            "This space will not judge you.\n"
            "It will simply stay with you — gently."
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
        "note": "If you want, you can share why:",
        "save": "Save today",
        "thanks": "Thank you for being honest with yourself.",
        "weekly": "Weekly Reflection",
        "weekly_locked": "This space will open gently after a few days.",
        "viewer": "Private Observer Mode",
        "password": "Password",
        "export": "Export PDF"
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (BRIGHT & CLEAN)
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
    font-size: 14px;
    line-height: 1.7;
}
button {
    border-radius: 18px !important;
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
# SCORE MAP
# ==================================================
SCORE_MAP = {0: 0, 1: 1, 2: 2, 3: 3}

# ==================================================
# LANGUAGE TOGGLE (VISIBLE TO ZARA)
# ==================================================
lang_col1, lang_col2 = st.columns([1,1])
with lang_col1:
    if st.button("🇮🇩"):
        st.session_state.lang = "id"
with lang_col2:
    if st.button("🇬🇧"):
        st.session_state.lang = "en"

# ==================================================
# CHECK VIEWER MODE (URL BASED)
# ==================================================
viewer_mode = st.query_params.get("viewer") == "true"

# ==================================================
# VIEWER MODE (PRIVATE)
# ==================================================
if viewer_mode:
    st.markdown(f"## {T['viewer']}")
    password = st.text_input(T["password"], type="password")

    if password == VIEWER_PASSWORD:
        st.subheader("Daily Journal (Full)")
        st.dataframe(daily_df)

        st.subheader("Weekly Reflections (Full)")
        st.dataframe(weekly_df)

        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(daily_df["date"]), daily_df["score"], marker="o")
        ax.set_yticks([0,1,2,3])
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        if st.button(T["export"]):
            fig_path = "progress.png"
            fig.savefig(fig_path)

            doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Zara’s Private Progress Report", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Image(fig_path, width=400, height=200))
            doc.build(story)

            st.download_button("⬇️ Download PDF", open(PDF_FILE, "rb"), file_name=PDF_FILE)
    else:
        st.warning("Access denied.")

# ==================================================
# PLAYER MODE (ZARA)
# ==================================================
else:
    if "read" not in st.session_state:
        st.session_state.read = False

    st.markdown(f"## 🌤️ {T['title']}")
    st.markdown(f"<p class='caption'>{T['landing']}</p>", unsafe_allow_html=True)

    st.checkbox(T["read"], key="read")

    if st.session_state.read:
        choice = st.radio(T["question"], T["choices"])
        note = st.text_area(T["note"], height=100)

        if st.button(T["save"]):
            today = datetime.now().strftime("%Y-%m-%d")
            score = T["choices"].index(choice)
            daily_df.loc[len(daily_df)] = [today, choice, note, score]
            daily_df.to_csv(DAILY_FILE, index=False)
            st.success(T["thanks"])
