import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import requests
from streamlit_lottie import st_lottie
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
    page_icon="🌙",
    layout="centered"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def go(page):
    st.session_state.page = page

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ==================================================
# THEME
# ==================================================
if st.session_state.theme == "light":
    BG, CARD, TEXT, SUB = "#fafaf9", "#ffffff", "#1f2937", "#6b7280"
else:
    BG, CARD, TEXT, SUB = "#0f1115", "#1a1d24", "#e5e7eb", "#9ca3af"

st.markdown(f"""
<style>
html, body, [class*="css"] {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Inter', sans-serif;
}}
.block-container {{
    max-width: 720px;
    padding-top: 2.5rem;
}}
.card {{
    background: {CARD};
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 30px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.05);
}}
.caption {{
    color: {SUB};
    font-size: 13px;
    line-height: 1.6;
    text-align: center;
}}
button {{ border-radius: 16px !important; }}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD CUTE ANIMATION
# ==================================================
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_companion = load_lottie(
    "https://assets1.lottiefiles.com/packages/lf20_touohxv0.json"
)

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
# SCORE MAP (INTERNAL ONLY)
# ==================================================
SCORE_MAP = {
    "I took my sleep medication": 1,
    "I delayed or reduced it": 2,
    "I didn’t need it today": 3,
    "Today felt heavy, I rested": 0
}

# ==================================================
# NAV BAR
# ==================================================
n1, n2, n3, n4 = st.columns([2,2,2,1])
with n1:
    if st.button("🌱 Zara"):
        go("journey")
with n2:
    if st.button("📝 Weekly"):
        go("weekly")
with n3:
    if st.button("👀 Care View"):
        go("viewer")
with n4:
    if st.button("🌓"):
        toggle_theme()

# ==================================================
# LANDING
# ==================================================
if st.session_state.page == "landing":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h1>🌙 Zara’s Gentle Space</h1>", unsafe_allow_html=True)
    st_lottie(lottie_companion, height=180)
    st.markdown("<p class='caption'>This space listens. It never judges.</p>", unsafe_allow_html=True)
    if st.button("Enter"):
        go("journey")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# DAILY JOURNEY
# ==================================================
elif st.session_state.page == "journey":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h2>🤍 {PLAYER_NAME}, how was today?</h2>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        list(SCORE_MAP.keys()),
        label_visibility="collapsed"
    )

    note = st.text_area(
        "If you want, you can share why:",
        placeholder="A few words are enough…",
        height=120
    )

    st_lottie(lottie_companion, height=160)

    if st.button("Save today"):
        today = datetime.now().strftime("%Y-%m-%d")
        score = SCORE_MAP[choice]
        daily_df.loc[len(daily_df)] = [today, choice, note, score]
        daily_df.to_csv(DAILY_FILE, index=False)
        st.success("Thank you for sharing, Zara.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# WEEKLY REFLECTION
# ==================================================
elif st.session_state.page == "weekly":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>📝 Weekly Reflection</h2>", unsafe_allow_html=True)

    heavy = st.text_area("What felt heavy this week?", height=90)
    helped = st.text_area("What helped, even a little?", height=90)
    carry = st.text_area("What would you like to carry forward?", height=90)

    if st.button("Save weekly reflection"):
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        weekly_df.loc[len(weekly_df)] = [week_start, heavy, helped, carry]
        weekly_df.to_csv(WEEKLY_FILE, index=False)
        st.success("Weekly reflection saved.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# VIEWER WITH GRAPH + PDF
# ==================================================
elif st.session_state.page == "viewer":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>👀 Care View</h2>", unsafe_allow_html=True)

    password = st.text_input("Password", type="password")
    if password == VIEWER_PASSWORD:

        st.subheader("📈 Gentle Progress Trend")
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(daily_df["date"]), daily_df["score"], marker="o")
        ax.set_ylabel("Gentle State (internal)")
        ax.set_xlabel("Date")
        st.pyplot(fig)

        st.subheader("🗒️ Daily Reflections")
        st.dataframe(daily_df[["date", "choice", "note"]])

        st.subheader("📝 Weekly Reflections")
        st.dataframe(weekly_df)

        # PDF EXPORT
        if st.button("📄 Export PDF"):
            fig_path = "progress.png"
            fig.savefig(fig_path)

            doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Zara’s Gentle Progress Report", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Image(fig_path, width=400, height=200))
            story.append(Spacer(1, 12))
            story.append(Paragraph("Weekly Reflections:", styles["Heading2"]))

            for _, row in weekly_df.iterrows():
                story.append(Paragraph(f"<b>Week of {row['week_start']}</b>", styles["Normal"]))
                story.append(Paragraph(f"Heavy: {row['heavy']}", styles["Normal"]))
                story.append(Paragraph(f"Helped: {row['helped']}", styles["Normal"]))
                story.append(Paragraph(f"Carry forward: {row['carry']}", styles["Normal"]))
                story.append(Spacer(1, 10))

            doc.build(story)
            st.success("PDF generated.")
            st.download_button("⬇️ Download PDF", open(PDF_FILE, "rb"), file_name=PDF_FILE)

    else:
        st.warning("Access restricted.")

    st.markdown("</div>", unsafe_allow_html=True)
