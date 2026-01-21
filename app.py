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
# LANGUAGE COPY
# ==================================================
TEXT = {
    "id": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "Sayang,\n\n"
            "Hari ini kamu tidak diminta menjadi apa pun.\n"
            "Tidak perlu lebih kuat, tidak perlu lebih baik.\n\n"
            "Ruang ini tidak ingin mengubahmu.\n"
            "Ia hanya ingin menemanimu.\n\n"
            "Kamu boleh masuk kapan pun kamu siap."
        ),
        "read": "Aku sudah membaca pesan ini",
        "start": "Awal",
        "daily_title": "Bagaimana hari ini terasa?",
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau kamu ingin, kamu boleh menuliskan sedikit ceritanya:",
        "save": "Simpan hari ini",
        "thank_title": "Terima kasih, Zara",
        "thank_text": (
            "Terima kasih sudah berhenti sejenak hari ini.\n\n"
            "Apa pun yang kamu pilih tadi,\n"
            "itu bukan ukuran keberhasilan atau kegagalan.\n\n"
            "Itu hanya cerminan dari apa yang kamu butuhkan.\n\n"
            "Ruang ini akan tetap ada.\n"
            "Tidak mendesak. Tidak menuntut."
        ),
        "back": "Kembali",
        "weekly_title": "Refleksi Mingguan",
        "weekly_info": "Bagian ini bukan evaluasi, hanya ruang melihat ke belakang dengan lembut.",
        "weekly_q1": "Apa yang terasa paling berat minggu ini?",
        "weekly_q2": "Apa yang sedikit membantu?",
        "weekly_q3": "Apa yang ingin kamu bawa ke minggu depan?",
        "weekly_save": "Simpan refleksi",
        "weekly_locked": "Refleksi mingguan akan terbuka setelah beberapa hari.",
        "viewer_title": "Mode Pemantau (Pribadi)",
        "password": "Password",
        "export": "Export PDF"
    },
    "en": {
        "title": "Zara’s Gentle Space",
        "landing": (
            "My love,\n\n"
            "Today, you are not asked to be anything.\n"
            "Not stronger. Not better.\n\n"
            "This space does not try to change you.\n"
            "It only wishes to stay with you.\n\n"
            "You may enter whenever you feel ready."
        ),
        "read": "I have read this message",
        "start": "Begin",
        "daily_title": "How did today feel?",
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you wish, you may share a little of what led to this:",
        "save": "Save today",
        "thank_title": "Thank you, Zara",
        "thank_text": (
            "Thank you for pausing today.\n\n"
            "Whatever you chose earlier\n"
            "is not a measure of success or failure.\n\n"
            "It simply reflects what you needed.\n\n"
            "This space remains.\n"
            "Quiet. Unrushed."
        ),
        "back": "Back",
        "weekly_title": "Weekly Reflection",
        "weekly_info": "This is not a review, just a gentle look back.",
        "weekly_q1": "What felt heaviest this week?",
        "weekly_q2": "What helped, even a little?",
        "weekly_q3": "What would you like to carry into next week?",
        "weekly_save": "Save reflection",
        "weekly_locked": "Weekly reflection will open after a few days.",
        "viewer_title": "Private Observer Mode",
        "password": "Password",
        "export": "Export PDF"
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (TIGHT & CLEAN)
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #fbfcfa;
    color: #1f2937;
    font-family: Inter, sans-serif;
}
.block-container {
    max-width: 700px;
    padding-top: 1.8rem;
}
.caption {
    color: #6b7280;
    font-size: 14.5px;
    line-height: 1.65;
}
button {
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE TOGGLE (TOP RIGHT)
# ==================================================
top_left, top_right = st.columns([5,1])
with top_right:
    lang = st.selectbox(
        "Language",
        ["Indonesia", "English"],
        index=0 if st.session_state.lang == "id" else 1,
        label_visibility="collapsed"
    )
    st.session_state.lang = "id" if lang == "Indonesia" else "en"

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
# VIEWER MODE (PRIVATE URL)
# ==================================================
viewer_mode = st.query_params.get("viewer") == "true"

if viewer_mode:
    st.markdown(f"## {T['viewer_title']}")
    password = st.text_input(T["password"], type="password")

    if password == VIEWER_PASSWORD:
        st.dataframe(daily_df)
        st.dataframe(weekly_df)

        if not daily_df.empty:
            fig, ax = plt.subplots()
            ax.plot(pd.to_datetime(daily_df["date"]), daily_df["score"], marker="o")
            ax.grid(alpha=0.3)
            st.pyplot(fig)

        if st.button(T["export"]):
            fig_path = "progress.png"
            fig.savefig(fig_path)
            doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [Paragraph("Zara’s Private Journal Summary", styles["Title"]), Spacer(1, 12), Image(fig_path, 400, 200)]
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
        st.markdown(f"## 🤍 {T['daily_title']}")
        choice = st.radio("", T["choices"])
        note = st.text_area(T["note"], height=100)
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

    elif st.session_state.page == "weekly":
        st.markdown(f"## {T['weekly_title']}")
        st.markdown(f"<p class='caption'>{T['weekly_info']}</p>", unsafe_allow_html=True)

        if not weekly_available:
            st.markdown(f"<p class='caption'>{T['weekly_locked']}</p>", unsafe_allow_html=True)
        else:
            heavy = st.text_area(T["weekly_q1"], height=80)
            helped = st.text_area(T["weekly_q2"], height=80)
            carry = st.text_area(T["weekly_q3"], height=80)

            if st.button(T["weekly_save"]):
                week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
                weekly_df.loc[len(weekly_df)] = [week_start, heavy, helped, carry]
                weekly_df.to_csv(WEEKLY_FILE, index=False)
                go("thanks")
