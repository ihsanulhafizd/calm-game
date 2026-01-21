import streamlit as st
from datetime import datetime

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="For Zara, Always",
    page_icon="💗",
    layout="centered"
)

# ==================================================
# LANGUAGE (URL SAFE, NO QUERY API)
# ==================================================
LANG = st.session_state.get("lang", "en")

def set_lang(l):
    st.session_state.lang = l
    st.rerun()

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
# STORY CONTENT (NOVEL STYLE)
# ==================================================
STORY = {
    "en": {
        "title": "For Zara, Always",
        "start": "Enter",
        "text": {
            "day": (
                "*The morning does not rush the room.*\n\n"
                "*It arrives the way stories begin — quietly, without demands.*\n\n"
                "*You don’t need to be ready all at once.*\n\n"
                "*This page exists only to stay with you.*"
            ),
            "night": (
                "*The evening closes like a book left open.*\n\n"
                "*Not finished — just resting between pages.*\n\n"
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
        }
    },
    "id": {
        "title": "Untuk Zara, Selalu",
        "start": "Masuk",
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
        }
    }
}

T = STORY[LANG]

# ==================================================
# STYLE + ICONS (SAFE CSS)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 640px;
    padding-top: 2.2rem;
}

p {
    font-style: italic;
    line-height: 1.9;
    font-size: 16px;
}

.novel p {
    font-family: 'Cormorant Garamond', serif;
    font-size: 18px;
    line-height: 2.1;
}

/* Language */
.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
}
.lang span {
    cursor: pointer;
    margin-left: 6px;
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
    animation: float 60s linear infinite;
}
.leaf {
    position: fixed;
    font-size: 14px;
    opacity: 0.25;
    animation: drift 70s linear infinite;
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

<div class="light" style="left:20%;"></div>
<div class="light" style="left:60%; animation-duration:80s;"></div>
<div class="leaf">🍃</div>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (REAL HORIZONTAL)
# ==================================================
st.markdown(
    f"""
    <div class="lang">
      <span class="{'active' if LANG=='en' else ''}" onclick="window.location.reload();">EN</span> |
      <span class="{'active' if LANG=='id' else ''}" onclick="window.location.reload();">ID</span>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1,1])
with col1:
    st.button("EN", on_click=set_lang, args=("en",))
with col2:
    st.button("ID", on_click=set_lang, args=("id",))

# ==================================================
# CONTENT
# ==================================================
st.markdown(f"## 💗 {T['title']}")
st.markdown(f"<div class='novel'>{T['text'][PHASE]}</div>", unsafe_allow_html=True)

st.button(T["start"])
