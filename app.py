import streamlit as st
from datetime import datetime
import pandas as pd
import os

# ==================================================
# BASIC CONFIG
# ==================================================
st.set_page_config(
    page_title="For Zara, Always",
    page_icon="💗",
    layout="centered"
)

DATA_FILE = "daily_journey.csv"

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "last_choice" not in st.session_state:
    st.session_state.last_choice = None

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
# CONTENT (NOVEL STYLE)
# ==================================================
CONTENT = {
    "en": {
        "title": "For Zara, Always",
        "start": "Enter",
        "daily_title": "How does today feel?",
        "landing": {
            "day": (
                "*The morning does not rush the room.*\n\n"
                "*It arrives slowly, like the opening of a novel.*\n\n"
                "*Nothing is demanded of you on this first page.*\n\n"
                "*You are allowed to read this moment gently.*"
            ),
            "night": (
                "*The evening settles like a book left open on the table.*\n\n"
                "*Not finished — only paused between chapters.*\n\n"
                "*You may loosen your grip now.*"
            ),
            "deep_night": (
                "*The room is quiet in a way that makes every breath noticeable.*\n\n"
                "*You do not need answers at this hour.*\n\n"
                "*Just stay.*"
            ),
            "very_late": (
                "*It is very late — the hour stories rarely describe.*\n\n"
                "*Nothing is expected of you now.*\n\n"
                "*Even staying awake counts as courage.*\n\n"
                "*I am here with you.*"
            )
        },
        "choices": [
            ("med", "I took my sleep medication"),
            ("delay", "I delayed or reduced it"),
            ("none", "I didn’t need it"),
            ("rest", "Today felt heavy, I rested")
        ],
        "thanks": {
            "med": (
                "*Thank you for choosing care tonight.*\n\n"
                "*Needing support does not mean you failed.*\n\n"
                "*Rest gently. You did enough.*"
            ),
            "delay": (
                "*You created a small pause today.*\n\n"
                "*That space matters more than it seems.*\n\n"
                "*I’m proud of you.*"
            ),
            "none": (
                "*Today your body carried you on its own.*\n\n"
                "*Notice that strength, quietly.*\n\n"
                "*Rest now.*"
            ),
            "rest": (
                "*You listened when the day felt heavy.*\n\n"
                "*Rest is not avoidance — it is wisdom.*\n\n"
                "*Thank you for honoring yourself.*"
            )
        }
    },
    "id": {
        "title": "Untuk Zara, Selalu",
        "start": "Masuk",
        "daily_title": "Bagaimana hari ini terasa?",
        "landing": {
            "day": (
                "*Pagi tidak pernah terburu-buru.*\n\n"
                "*Ia datang seperti awal cerita — pelan dan tanpa tuntutan.*\n\n"
                "*Tidak ada yang diminta darimu di halaman pertama ini.*\n\n"
                "*Kamu boleh membacanya dengan lembut.*"
            ),
            "night": (
                "*Malam turun seperti buku yang dibiarkan terbuka.*\n\n"
                "*Belum selesai — hanya berhenti sejenak.*\n\n"
                "*Kamu boleh melepaskan genggamanmu.*"
            ),
            "deep_night": (
                "*Ruangan sunyi dengan cara yang membuat napas terasa nyata.*\n\n"
                "*Kamu tidak perlu jawaban di jam ini.*\n\n"
                "*Cukup ada.*"
            ),
            "very_late": (
                "*Ini sudah sangat larut — jam yang jarang ditulis dalam cerita.*\n\n"
                "*Tidak ada tuntutan apa pun darimu sekarang.*\n\n"
                "*Bertahan saja sudah cukup.*\n\n"
                "*Aku di sini bersamamu.*"
            )
        },
        "choices": [
            ("med", "Aku minum obat tidur"),
            ("delay", "Aku menunda atau mengurangi"),
            ("none", "Aku tidak membutuhkannya"),
            ("rest", "Hari ini terasa berat, aku beristirahat")
        ],
        "thanks": {
            "med": (
                "*Terima kasih sudah memilih merawat diri malam ini.*\n\n"
                "*Membutuhkan bantuan bukan kegagalan.*\n\n"
                "*Istirahatlah dengan lembut.*"
            ),
            "delay": (
                "*Kamu memberi jeda hari ini.*\n\n"
                "*Ruang kecil itu berarti.*\n\n"
                "*Aku bangga padamu.*"
            ),
            "none": (
                "*Hari ini tubuhmu menopangmu sendiri.*\n\n"
                "*Sadari kekuatan itu — pelan-pelan.*\n\n"
                "*Sekarang beristirahatlah.*"
            ),
            "rest": (
                "*Kamu mendengar saat hari terasa berat.*\n\n"
                "*Istirahat bukan menyerah — itu kebijaksanaan.*\n\n"
                "*Terima kasih sudah jujur pada dirimu.*"
            )
        }
    }
}

T = CONTENT[st.session_state.lang]

# ==================================================
# STYLE + ICONS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 640px;
    padding-top: 2rem;
}

p {
    font-style: italic;
    font-size: 17px;
    line-height: 2;
}

.novel p {
    font-family: 'Cormorant Garamond', serif;
    font-size: 19px;
}

/* Language switch */
.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
}
.lang span {
    cursor: pointer;
    margin: 0 4px;
    color: #9ca3af;
}
.lang .active {
    color: #111827;
    font-weight: 600;
}

/* Icons */
.light {
    position: fixed;
    width: 6px;
    height: 6px;
    background: rgba(255,255,255,0.35);
    border-radius: 50%;
    animation: float 70s linear infinite;
}
.leaf {
    position: fixed;
    font-size: 14px;
    opacity: 0.25;
    animation: drift 80s linear infinite;
}

@keyframes float {
    from { transform: translate(-10vw,110vh); }
    to { transform: translate(110vw,-10vh); }
}
@keyframes drift {
    from { transform: translate(110vw,30vh) rotate(0deg); }
    to { transform: translate(-10vw,70vh) rotate(360deg); }
}
</style>

<div class="lang">
  <span class="{en}" onclick="document.getElementById('lang_en').click()">EN</span> |
  <span class="{id}" onclick="document.getElementById('lang_id').click()">ID</span>
</div>

<div class="light" style="left:25%;"></div>
<div class="light" style="left:65%; animation-duration:90s;"></div>
<div class="leaf">🍃</div>
""".format(
    en="active" if st.session_state.lang == "en" else "",
    id="active" if st.session_state.lang == "id" else ""
), unsafe_allow_html=True)

# Hidden language triggers
st.button("EN", key="lang_en", on_click=lambda: st.session_state.update(lang="en"))
st.button("ID", key="lang_id", on_click=lambda: st.session_state.update(lang="id"))

# ==================================================
# DATA INIT
# ==================================================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "choice"]).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# ==================================================
# PAGE FLOW
# ==================================================
st.markdown(f"## 💗 {T['title']}")

# --- LANDING ---
if st.session_state.page == "landing":
    st.markdown(f"<div class='novel'>{T['landing'][PHASE]}</div>", unsafe_allow_html=True)
    if st.button(T["start"]):
        st.session_state.page = "daily"
        st.rerun()

# --- DAILY ---
elif st.session_state.page == "daily":
    st.markdown(f"### {T['daily_title']}")
    labels = [lbl for _, lbl in T["choices"]]
    keys = [k for k, _ in T["choices"]]
    idx = st.radio("", range(len(labels)), format_func=lambda i: labels[i])
    if st.button("Continue"):
        st.session_state.last_choice = keys[idx]
        df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d"), labels[idx]]
        df.to_csv(DATA_FILE, index=False)
        st.session_state.page = "thanks"
        st.rerun()

# --- THANK YOU ---
elif st.session_state.page == "thanks":
    msg = T["thanks"][st.session_state.last_choice]
    st.markdown(msg)
    st.markdown("\n\n*Thank you for being here. You are not alone.*")
