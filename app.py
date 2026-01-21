import streamlit as st
from datetime import datetime
import pandas as pd
import os

# ==================================================
# LANGUAGE FROM QUERY PARAM (INLINE EN | ID)
# ==================================================
params = st.query_params
if "lang" not in params:
    params["lang"] = "en"
LANG = params["lang"]

# ==================================================
# CONFIG
# ==================================================
APP_TITLE = "For Zara, Always"
DATA_FILE = "daily_journey.csv"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💗",
    layout="centered"
)

# ==================================================
# SESSION
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def go(p):
    st.session_state.page = p

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
# NOVEL STORIES
# ==================================================
STORY = {
    "en": {
        "title": "For Zara, Always",
        "text": {
            "day": (
                "*The morning does not rush the room.*\n\n"
                "*It arrives the way stories begin — quietly, without demands.*\n\n"
                "*You don’t need to be ready all at once.*\n\n"
                "*This page exists only to be read, not to judge you.*"
            ),
            "night": (
                "*The evening closes around you like a book left open.*\n\n"
                "*Not finished — only paused.*\n\n"
                "*You may loosen your grip now.*"
            ),
            "deep_night": (
                "*The world is still in a way that makes every breath noticeable.*\n\n"
                "*You don’t need clarity in this chapter.*\n\n"
                "*Just stay.*"
            ),
            "very_late": (
                "*It is very late — the hour most novels never describe.*\n\n"
                "*Nothing is expected of you now.*\n\n"
                "*Even staying awake counts as courage.*\n\n"
                "*I am here.*"
            )
        },
        "start": "Enter"
    },
    "id": {
        "title": "Untuk Zara, Selalu",
        "text": {
            "day": (
                "*Pagi tidak pernah terburu-buru.*\n\n"
                "*Ia datang seperti awal cerita — pelan dan tanpa tuntutan.*\n\n"
                "*Kamu tidak perlu siap sekaligus.*\n\n"
                "*Halaman ini hanya ingin menemanimu.*"
            ),
            "night": (
                "*Malam menutupmu seperti buku yang dibiarkan terbuka.*\n\n"
                "*Belum selesai — hanya berhenti sejenak.*"
            ),
            "deep_night": (
                "*Dunia sunyi dengan cara yang membuat napas terasa nyata.*\n\n"
                "*Kamu tidak perlu kejelasan di bab ini.*"
            ),
            "very_late": (
                "*Ini sangat larut — jam yang jarang ditulis dalam cerita.*\n\n"
                "*Tidak ada harapan apa pun darimu sekarang.*\n\n"
                "*Bertahan saja sudah cukup.*\n\n"
                "*Aku di sini.*"
            )
        },
        "start": "Masuk"
    }
}

T = STORY[LANG]

# ==================================================
# STYLE (NOVEL OPENING + ICONS)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Landing page novel feel */
.novel p {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 18px;
    line-height: 2.1;
}

/* Other pages */
p {
    font-style: italic;
    line-height: 1.9;
    font-size: 16px;
}

.block-container {
    max-width: 640px;
    padding-top: 2.2rem;
}

/* Language switch */
.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
}
.lang a {
    text-decoration: none;
    margin-left: 6px;
    color: #9ca3af;
}
.lang a.active {
    color: #111827;
    font-weight: 600;
}

/* ICON LAYERS */
.light, .dust {
    position: fixed;
    border-radius: 50%;
    background: rgba(255,255,255,0.35);
    animation: float 50s linear infinite;
}

.light {
    width: 6px;
    height: 6px;
}

.dust {
    width: 3px;
    height: 3px;
    opacity: 0.3;
    animation-duration: 70s;
}

.leaf {
    position: fixed;
    font-size: 14px;
    opacity: 0.25;
    animation: drift 60s linear infinite;
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
  <a href="?lang=en" class="{en}">EN</a> |
  <a href="?lang=id" class="{id}">ID</a>
</div>

<div class="light" style="left:15%;"></div>
<div class="light" style="left:55%; animation-duration:60s;"></div>
<div class="dust" style="left:35%;"></div>
<div class="dust" style="left:75%; animation-duration:80s;"></div>
<div class="leaf">🍃</div>
""".format(
    en="active" if LANG == "en" else "",
    id="active" if LANG == "id" else ""
), unsafe_allow_html=True)

# ==================================================
# DATA INIT
# ==================================================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date","note"]).to_csv(DATA_FILE, index=False)

# ==================================================
# FLOW
# ==================================================
st.markdown(f"## 💗 {T['title']}")

if st.session_state.page == "landing":
    st.markdown(f"<div class='novel'>{T['text'][PHASE]}</div>", unsafe_allow_html=True)
    if st.button(T["start"]):
        go("daily")
