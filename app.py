import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# CONFIG
# ==================================================
APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"

VIEWER_PASSWORD = "06september2025"

DATA_FILE = "daily_journey.csv"

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
if "viewer_auth" not in st.session_state:
    st.session_state.viewer_auth = False

def go(p):
    st.session_state.page = p

# ==================================================
# TIME LOGIC
# ==================================================
now = datetime.now()
hour = now.hour
today_str = now.strftime("%d %B")

def phase():
    if 0 <= hour < 6:
        return "deep"
    elif 18 <= hour <= 23:
        return "night"
    return "day"

PHASE = phase()

# ==================================================
# BOOK-STYLE MESSAGES
# ==================================================
MESSAGES = {
    "en": {
        "day": """This page opens gently.

You are not expected to be better here.
You are not expected to understand anything yet.

This is a place to sit with what exists today.
Nothing more.
Nothing less.

Take your time.
I am here.""",

        "night": """The night has arrived quietly.

If your thoughts feel louder now,
you do not need to silence them.

This page does not ask for answers.
It only offers company.

Lay down what you carried today.
You are not alone in this.""",

        "deep": """It is very late now.

The world is mostly asleep,
and it can feel lonely to still be awake.

You do not need clarity in this hour.
You do not need to fix tomorrow tonight.

Just breathe.
Just exist.

This page stays with you."""
    },
    "id": {
        "day": """Halaman ini terbuka dengan pelan.

Tidak ada tuntutan di sini.
Tidak ada yang perlu kamu pahami hari ini.

Ruang ini hanya ingin menemanimu
apa adanya.

Ambil waktumu.
Aku di sini.""",

        "night": """Malam datang dengan sunyi.

Jika pikiranmu terasa lebih ramai sekarang,
kamu tidak perlu melawannya.

Halaman ini tidak meminta jawaban.
Ia hanya menemani.

Letakkan beban hari ini.
Kamu tidak sendirian.""",

        "deep": """Sekarang sudah sangat larut.

Dunia hampir sepenuhnya tertidur,
dan itu bisa terasa sepi.

Kamu tidak perlu memahami apa pun malam ini.
Kamu tidak perlu menyelesaikan apa pun.

Bernapaslah.
Cukup ada.

Halaman ini tetap di sini."""
    }
}

# ==================================================
# STYLES (MAX AESTHETIC)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.block-container {
    max-width: 680px;
    padding-top: 2rem;
}

p {
    font-style: italic;
    font-size: 16px;
    line-height: 2;
}

.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
    opacity: 0.85;
}

.lang span {
    cursor: pointer;
    margin-left: 6px;
}

.active { font-weight: 600; }
.inactive { opacity: 0.4; }

/* Fireflies */
.firefly {
    position: fixed;
    width: 5px;
    height: 5px;
    background: rgba(255,255,255,0.35);
    border-radius: 50%;
    filter: blur(1px);
    animation: drift 50s linear infinite;
}

@keyframes drift {
    from { transform: translate(-10vw, 110vh); opacity: 0; }
    to { transform: translate(110vw, -10vh); opacity: 0.4; }
}
</style>

<div class="firefly" style="left:15%; animation-duration:55s;"></div>
<div class="firefly" style="left:50%; animation-duration:65s;"></div>
<div class="firefly" style="left:80%; animation-duration:60s;"></div>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH
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
# DATA INIT
# ==================================================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "time", "choice", "note"]).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# ==================================================
# VIEWER MODE (PRIVATE)
# ==================================================
if st.query_params.get("viewer") == "true":
    st.markdown("## 🔐 Private Viewer")

    if not st.session_state.viewer_auth:
        pw = st.text_input("Password", type="password")
        if pw == VIEWER_PASSWORD:
            st.session_state.viewer_auth = True
            st.experimental_rerun()
        st.stop()

    st.markdown("### 📖 Zara’s Journey Overview")

    st.markdown(
        "<p style='font-style:italic'>This view exists only for understanding, never for control.</p>",
        unsafe_allow_html=True
    )

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.markdown("### ⏳ Timeline")
        st.line_chart(df.groupby("date").size())

    st.stop()

# ==================================================
# USER FLOW (ZARA)
# ==================================================
if st.session_state.page == "landing":
    st.markdown(f"## 💗 {APP_TITLE_EN if st.session_state.lang=='en' else APP_TITLE_ID}")
    st.markdown(MESSAGES[st.session_state.lang][PHASE])
    if st.button("Turn the page" if st.session_state.lang=="en" else "Buka halaman"):
        go("daily")

elif st.session_state.page == "daily":
    st.markdown("### How does today feel?" if st.session_state.lang=="en" else "Bagaimana hari ini terasa?")
    choice = st.radio("", [
        "I took my sleep medication",
        "I delayed or reduced it",
        "I didn’t need it",
        "Today felt heavy, I rested"
    ] if st.session_state.lang=="en" else [
        "Aku minum obat tidur",
        "Aku menunda atau mengurangi",
        "Aku tidak membutuhkannya",
        "Hari ini terasa berat, aku beristirahat"
    ])
    note = st.text_area("You can write anything here:" if st.session_state.lang=="en" else "Kamu bisa menulis apa pun di sini:", height=160)
    if st.button("Save" if st.session_state.lang=="en" else "Simpan"):
        df.loc[len(df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            choice,
            note
        ]
        df.to_csv(DATA_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(
        "*Thank you for turning this page today.*" if st.session_state.lang=="en"
        else "*Terima kasih sudah membuka halaman ini hari ini.*"
    )
    if st.button("Close"):
        go("landing")
