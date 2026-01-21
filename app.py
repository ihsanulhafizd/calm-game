import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="For Zara, Always",
    page_icon="💗",
    layout="centered"
)

DATA_FILE = "daily_journey.csv"
VIEWER_PASSWORD = "06september2025"

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "last_choice" not in st.session_state:
    st.session_state.last_choice = None
if "viewer_ok" not in st.session_state:
    st.session_state.viewer_ok = False

# ==================================================
# INIT DATA
# ==================================================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "time", "choice"]).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# ==================================================
# TIME PHASE
# ==================================================
hour = datetime.now().hour
if 1 <= hour <= 3:
    PHASE = "very_late"
elif hour == 0 or 4 <= hour <= 5:
    PHASE = "deep_night"
elif 18 <= hour <= 23:
    PHASE = "night"
else:
    PHASE = "day"

# ==================================================
# CONTENT
# ==================================================
CONTENT = {
    "en": {
        "title": "For Zara, Always",
        "start": "Enter",
        "daily": "How does today feel?",
        "landing": {
            "day": "*The morning does not rush the room...*",
            "night": "*The evening settles like a book left open...*",
            "deep_night": "*The room is quiet in a way that makes breathing louder...*",
            "very_late": "*It is very late — the hour stories rarely describe...*"
        },
        "choices": [
            ("med", "I took my sleep medication"),
            ("delay", "I delayed or reduced it"),
            ("none", "I didn’t need it"),
            ("rest", "Today felt heavy, I rested")
        ],
        "thanks": {
            "med": "*Thank you for choosing care tonight...*",
            "delay": "*You created a pause today...*",
            "none": "*Today your body carried you on its own...*",
            "rest": "*You listened when today felt heavy...*"
        }
    },
    "id": {
        "title": "Untuk Zara, Selalu",
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "landing": {
            "day": "*Pagi tidak pernah terburu-buru...*",
            "night": "*Malam turun seperti buku yang dibiarkan terbuka...*",
            "deep_night": "*Ruangan sunyi dengan cara yang membuat napas terasa nyata...*",
            "very_late": "*Ini sudah sangat larut — jam yang jarang ditulis dalam cerita...*"
        },
        "choices": [
            ("med", "Aku minum obat tidur"),
            ("delay", "Aku menunda atau mengurangi"),
            ("none", "Aku tidak membutuhkannya"),
            ("rest", "Hari ini terasa berat, aku beristirahat")
        ],
        "thanks": {
            "med": "*Terima kasih sudah memilih merawat diri malam ini...*",
            "delay": "*Kamu memberi jeda hari ini...*",
            "none": "*Hari ini tubuhmu menopangmu sendiri...*",
            "rest": "*Kamu mendengar saat hari terasa berat...*"
        }
    }
}

T = CONTENT[st.session_state.lang]

# ==================================================
# STYLE
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&family=Inter:wght@300;400&display=swap');
.block-container { max-width: 640px; padding-top: 2rem; }
p { font-style: italic; font-size: 17px; line-height: 2; }
.novel p { font-family: 'Cormorant Garamond', serif; font-size: 19px; }
.lang { position: fixed; top: 14px; right: 18px; font-size: 11px; }
.lang span { margin: 0 4px; cursor: pointer; color: #9ca3af; }
.lang .active { color: #111827; font-weight: 600; }
</style>

<div class="lang">
  <span class="{en}" onclick="document.getElementById('en').click()">EN</span> |
  <span class="{id}" onclick="document.getElementById('id').click()">ID</span>
</div>
""".format(
    en="active" if st.session_state.lang=="en" else "",
    id="active" if st.session_state.lang=="id" else ""
), unsafe_allow_html=True)

st.button("EN", key="en", on_click=lambda: st.session_state.update(lang="en"))
st.button("ID", key="id", on_click=lambda: st.session_state.update(lang="id"))

# ==================================================
# VIEWER MODE
# ==================================================
if "viewer" in st.query_params:
    if not st.session_state.viewer_ok:
        pwd = st.text_input("Viewer Password", type="password")
        if st.button("Enter"):
            if pwd == VIEWER_PASSWORD:
                st.session_state.viewer_ok = True
                st.rerun()
        st.stop()

    st.title("📊 Viewer Dashboard")
    st.dataframe(df)
    st.line_chart(df["choice"].value_counts())
    st.stop()

# ==================================================
# PLAYER FLOW
# ==================================================
st.markdown(f"## 💗 {T['title']}")

if st.session_state.page == "landing":
    st.markdown(f"<div class='novel'>{T['landing'][PHASE]}</div>", unsafe_allow_html=True)
    if st.button(T["start"]):
        st.session_state.page = "daily"
        st.rerun()

elif st.session_state.page == "daily":
    st.markdown(f"### {T['daily']}")
    labels = [lbl for _, lbl in T["choices"]]
    keys = [k for k, _ in T["choices"]]
    idx = st.radio("", range(len(labels)), format_func=lambda i: labels[i])
    if st.button("Continue"):
        st.session_state.last_choice = keys[idx]
        df.loc[len(df)] = [
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M"),
            labels[idx]
        ]
        df.to_csv(DATA_FILE, index=False)
        st.session_state.page = "thanks"
        st.rerun()

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"][st.session_state.last_choice])
    st.markdown("*Thank you for being here. You are not alone.*")
