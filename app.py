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
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"

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
# STORY CONTENT
# ==================================================
STORY = {
    "en": {
        "title": "For Zara, Always",
        "start": "Enter",
        "daily_title": "How does today feel?",
        "text": {
            "day": (
                "*The morning does not rush the room.*\n\n"
                "*It arrives quietly, like the first page of a book.*\n\n"
                "*You don’t need to be ready all at once.*"
            ),
            "night": (
                "*The evening closes like a book left open.*\n\n"
                "*Not finished — just resting between pages.*"
            ),
            "deep_night": (
                "*The world is still in a way that makes breathing louder.*\n\n"
                "*You don’t need answers now.*"
            ),
            "very_late": (
                "*It is very late.*\n\n"
                "*Staying awake already counts as courage.*\n\n"
                "*I am here.*"
            )
        }
    },
    "id": {
        "title": "Untuk Zara, Selalu",
        "start": "Masuk",
        "daily_title": "Bagaimana hari ini terasa?",
        "text": {
            "day": (
                "*Pagi tidak pernah terburu-buru.*\n\n"
                "*Ia datang pelan, seperti halaman pertama cerita.*\n\n"
                "*Kamu tidak perlu siap sekaligus.*"
            ),
            "night": (
                "*Malam menutup seperti buku yang dibiarkan terbuka.*\n\n"
                "*Belum selesai — hanya berhenti sejenak.*"
            ),
            "deep_night": (
                "*Dunia sunyi dengan cara yang membuat napas terasa nyata.*\n\n"
                "*Kamu tidak perlu jawaban sekarang.*"
            ),
            "very_late": (
                "*Ini sangat larut.*\n\n"
                "*Bertahan saja sudah berarti.*\n\n"
                "*Aku di sini.*"
            )
        }
    }
}

T = STORY[st.session_state.lang]

# ==================================================
# STYLE (LANG SPACING FIXED)
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
    margin: 0 4px; /* ~3mm spacing */
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

<div class="lang">
  <span class="{en}" onclick="document.getElementById('lang_en').click()">EN</span> |
  <span class="{id}" onclick="document.getElementById('lang_id').click()">ID</span>
</div>

<div class="light" style="left:25%;"></div>
<div class="light" style="left:65%; animation-duration:85s;"></div>
<div class="leaf">🍃</div>
""".format(
    en="active" if st.session_state.lang == "en" else "",
    id="active" if st.session_state.lang == "id" else ""
), unsafe_allow_html=True)

# Hidden language triggers
st.button("EN", key="lang_en", on_click=lambda: st.session_state.update(lang="en"))
st.button("ID", key="lang_id", on_click=lambda: st.session_state.update(lang="id"))

# ==================================================
# PAGE FLOW
# ==================================================
st.markdown(f"## 💗 {T['title']}")

if st.session_state.page == "landing":
    st.markdown(f"<div class='novel'>{T['text'][PHASE]}</div>", unsafe_allow_html=True)
    if st.button(T["start"]):
        st.session_state.page = "daily"
        st.rerun()

elif st.session_state.page == "daily":
    st.markdown(f"### {T['daily_title']}")
    st.markdown(T["text"][PHASE])
    st.radio(
        "",
        ["Option 1", "Option 2", "Option 3"],
        label_visibility="collapsed"
    )
