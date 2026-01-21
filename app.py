import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
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
    page_icon="🌤️",
    layout="centered"
)

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def go(page):
    st.session_state.page = page

# ==================================================
# BRIGHT & AIRY STYLE (NO CARDS)
# ==================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #fbfcfa;
    color: #1f2937;
    font-family: 'Inter', sans-serif;
}
.block-container {
    max-width: 720px;
    padding-top: 2.5rem;
}
h1, h2 {
    font-weight: 600;
}
.caption {
    color: #6b7280;
    font-size: 13px;
    line-height: 1.6;
}
button {
    border-radius: 18px !important;
}
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD ONE CUTE ANIMATION
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
# WEEKLY AVAILABILITY CHECK
# ==================================================
weekly_available = False
if not daily_df.empty:
    first_day = pd.to_datetime(daily_df["date"]).min()
    if (datetime.now() - first_day).days >= 7:
        weekly_available = True

# ==================================================
# NAV BAR
# ==================================================
nav1, nav2, nav3 = st.columns([2,2,2])
with nav1:
    if st.button("🌱 Zara"):
        go("journey")
with nav2:
    if st.button("📝 Weekly"):
        go("weekly")
with nav3:
    if st.button("👀 Care View"):
        go("viewer")

st.markdown("<hr>", unsafe_allow_html=True)

# ==================================================
# LANDING
# ==================================================
if st.session_state.page == "landing":
    st.markdown("## 🌤️ Zara’s Gentle Space")
    st_lottie(lottie_companion, height=180)
    st.markdown(
        "<p class='caption'>A light place. Nothing to fix. Nothing to prove.</p>",
        unsafe_allow_html=True
    )
    if st.button("Enter"):
        go("journey")

# ==================================================
# DAILY JOURNEY
# ==================================================
elif st.session_state.page == "journey":
    st.markdown(f"## 🤍 Hi Zara")
    st.markdown("<p class='caption'>How did today feel?</p>", unsafe_allow_html=True)

    choice = st.radio(
        "",
        list(SCORE_MAP.keys()),
        label_visibility="collapsed"
    )

    note = st.text_area(
        "If you want, you can share a little why:",
        placeholder="A few words are enough…",
        height=110
    )

    st_lottie(lottie_companion, height=150)

    if st.button("Save today"):
        today = datetime.now().strftime("%Y-%m-%d")
        score = SCORE_MAP[choice]
        daily_df.loc[len(daily_df)] = [today, choice, note, score]
        daily_df.to_csv(DAILY_FILE, index=False)
        st.success("Thank you for sharing, Zara.")

# ==================================================
# WEEKLY REFLECTION (LOCKED UNTIL 7 DAYS)
# ==================================================
elif st.session_state.page == "weekly":
    st.markdown("## 📝 Weekly Reflection")

    if not weekly_available:
        st.markdown(
            "<p class='caption'>This space will open gently after a few days of journaling.</p>",
            unsafe_allow_html=True
        )
    else:
        heavy = st.text_area("What felt heavy this week?", height=90)
        helped = st.text_area("What helped, even a little?", height=90)
        carry = st.text_area("What would you like to carry forward?", height=90)

        if st.button("Save weekly reflection"):
            week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
            weekly_df.loc[len(weekly_df)] = [week_start, heavy, helped, carry]
            weekly_df.to_csv(WEEKLY_FILE, index=False)
            st.success("Your week has been gently recorded.")

# ==================================================
# VIEWER WITH GRAPH + PDF
# ==================================================
elif st.session_state.page == "viewer":
    st.markdown("## 👀 Care View")

    password = st.text_input("Password", type="password")
    if password == VIEWER_PASSWORD:

        st.markdown("### 📈 Gentle Trend")
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(daily_df["date"]), daily_df["score"], marker="o")
        ax.set_yticks([0,1,2,3])
        ax.set_ylabel("Gentle state")
        ax.set_xlabel("Date")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        st.markdown("### 🗒️ Daily Reflections")
        st.dataframe(daily_df[["date", "choice", "note"]])

        st.markdown("### 📝 Weekly Reflections")
        st.dataframe(weekly_df)

        if st.button("📄 Export PDF"):
            fig_path = "progress.png"
            fig.savefig(fig_path)

            doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Zara’s Gentle Progress", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Image(fig_path, width=400, height=200))
            story.append(Spacer(1, 12))

            for _, row in weekly_df.iterrows():
                story.append(Paragraph(f"<b>Week of {row['week_start']}</b>", styles["Normal"]))
                story.append(Paragraph(f"Heavy: {row['heavy']}", styles["Normal"]))
                story.append(Paragraph(f"Helped: {row['helped']}", styles["Normal"]))
                story.append(Paragraph(f"Carry: {row['carry']}", styles["Normal"]))
                story.append(Spacer(1, 10))

            doc.build(story)
            st.success("PDF ready.")
            st.download_button("⬇️ Download PDF", open(PDF_FILE, "rb"), file_name=PDF_FILE)

    else:
        st.warning("Access restricted.")
