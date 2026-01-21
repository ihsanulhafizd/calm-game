import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================================
# CONFIG
# ==================================================
APP_TITLE_EN = "For Zara, Always"
APP_TITLE_ID = "Untuk Zara, Selalu"
DAILY_FILE = "daily_journey.csv"

st.set_page_config(
    page_title=APP_TITLE_EN,
    page_icon="💗",
    layout="centered"
)

# ==================================================
# STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "last_choice" not in st.session_state:
    st.session_state.last_choice = None

def go(p):
    st.session_state.page = p

# ==================================================
# TIME PHASE
# ==================================================
now = datetime.now()
hour = now.hour
today_str = now.strftime("%d %B")

def time_phase(h):
    if 1 <= h <= 3:
        return "very_late_night"
    if h == 0 or 4 <= h <= 5:
        return "deep_night"
    if 18 <= h <= 23:
        return "night"
    return "day"

PHASE = time_phase(hour)

# ==================================================
# NOVEL-STYLE STORIES (EN)
# ==================================================
STORY_EN = {
    "day": (
        "*Morning light does not rush the room.*\n\n"
        "*It arrives slowly, touching the edges of things before asking anything of them.*\n\n"
        "*Today can be like that.*\n"
        "*You don’t need to be ready all at once.*\n\n"
        "*If your thoughts wander ahead of you, let them.*\n"
        "*If your body asks for pauses, listen.*\n\n"
        "*There is no wrong pace here.*\n"
        "*Only the one that keeps you breathing.*"
    ),
    "night": (
        "*The evening settles the way a book closes halfway.*\n\n"
        "*Not finished—just resting between chapters.*\n\n"
        "*Whatever the day asked of you can wait now.*\n"
        "*The noise softens. The edges blur.*\n\n"
        "*Tonight is not for fixing.*\n"
        "*It is for loosening your grip.*\n\n"
        "*I’m here, sitting quietly beside you.*"
    ),
    "deep_night": (
        "*The room is quiet now.*\n\n"
        "*Not empty—just still.*\n\n"
        "*This kind of quiet can make thoughts louder.*\n"
        "*That doesn’t mean you have to follow them.*\n\n"
        "*You don’t need clarity at this hour.*\n"
        "*Only rest.*\n\n"
        "*You are allowed to simply exist.*"
    ),
    "very_late_night": (
        "*It’s very late, the hour most stories never describe.*\n\n"
        "*The world is asleep, but you are still here.*\n"
        "*That alone is enough.*\n\n"
        "*Nothing needs to be decided tonight.*\n"
        "*Nothing needs to be solved.*\n\n"
        "*Wrap yourself in the smallest comforts.*\n"
        "*Even breathing counts as progress now.*\n\n"
        "*I won’t leave you alone in this chapter.*"
    )
}

# ==================================================
# NOVEL-STYLE STORIES (ID)
# ==================================================
STORY_ID = {
    "day": (
        "*Cahaya pagi tidak pernah terburu-buru.*\n\n"
        "*Ia datang perlahan, menyentuh sudut-sudut sebelum meminta apa pun.*\n\n"
        "*Hari ini bisa seperti itu.*\n"
        "*Kamu tidak harus siap sekaligus.*\n\n"
        "*Jika pikiranmu melayang jauh, biarkan.*\n"
        "*Jika tubuhmu meminta jeda, dengarkan.*\n\n"
        "*Tidak ada ritme yang salah di sini.*\n"
        "*Hanya ritme yang membuatmu tetap bernapas.*"
    ),
    "night": (
        "*Malam turun seperti buku yang ditutup setengah.*\n\n"
        "*Belum selesai—hanya beristirahat di antara bab.*\n\n"
        "*Apa pun yang diminta hari ini bisa menunggu.*\n"
        "*Suara melembut. Garis-garis mengabur.*\n\n"
        "*Malam ini bukan untuk memperbaiki.*\n"
        "*Malam ini untuk melepaskan.*\n\n"
        "*Aku duduk diam di sampingmu.*"
    ),
    "deep_night": (
        "*Ruangan kini sunyi.*\n\n"
        "*Bukan kosong—hanya tenang.*\n\n"
        "*Sunyi seperti ini kadang membuat pikiran lebih keras.*\n"
        "*Itu tidak berarti kamu harus mengikutinya.*\n\n"
        "*Kamu tidak perlu kejelasan di jam ini.*\n"
        "*Cukup istirahat.*"
    ),
    "very_late_night": (
        "*Ini sudah sangat larut, jam yang jarang ditulis dalam cerita.*\n\n"
        "*Dunia tertidur, tapi kamu masih ada di sini.*\n"
        "*Itu sudah cukup.*\n\n"
        "*Tidak ada keputusan malam ini.*\n"
        "*Tidak ada jawaban yang harus ditemukan.*\n\n"
        "*Selimuti dirimu dengan hal-hal kecil yang menenangkan.*\n"
        "*Bernapas saja sudah berarti.*\n\n"
        "*Aku tidak akan meninggalkanmu di bab ini.*"
    )
}

# ==================================================
# TEXT MAP
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": STORY_EN["day"],
        "start": "Enter",
        "daily": "How does today feel?",
        "story": STORY_EN[PHASE],
        "choices": [
            ("med", "I took my sleep medication"),
            ("delay", "I delayed or reduced it"),
            ("none", "I didn’t need it"),
            ("rest", "Today felt heavy, I rested")
        ],
        "note": "You can write anything here:",
        "save": "Save",
        "thanks": "*Thank you for turning this page today.*"
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": STORY_ID["day"],
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "story": STORY_ID[PHASE],
        "choices": [
            ("med", "Aku minum obat tidur"),
            ("delay", "Aku menunda atau mengurangi"),
            ("none", "Aku tidak membutuhkannya"),
            ("rest", "Hari ini terasa berat, aku beristirahat")
        ],
        "note": "Kamu bisa menulis apa pun di sini:",
        "save": "Simpan",
        "thanks": "*Terima kasih sudah membuka halaman ini hari ini.*"
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE + ICONS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,500&family=Inter:wght@300;400&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.block-container {
    max-width: 640px;
    padding-top: 2rem;
}

p {
    font-style: italic;
    line-height: 1.9;
    font-size: 16px;
}

/* Language switch */
.lang {
    position: fixed;
    top: 14px;
    right: 18px;
    font-size: 11px;
    opacity: .85;
}
.lang span {
    cursor: pointer;
    margin-left: 6px;
}
.active { font-weight: 600; }
.inactive { opacity: .5; }

/* Particles */
.light {
    position: fixed;
    width: 6px;
    height: 6px;
    background: rgba(255,255,255,0.4);
    border-radius: 50%;
    animation: float 40s linear infinite;
}
.leaf {
    position: fixed;
    font-size: 14px;
    opacity: 0.25;
    animation: drift 55s linear infinite;
}

@keyframes float {
    from { transform: translate(-10vw,110vh); }
    to { transform: translate(110vw,-10vh); }
}
@keyframes drift {
    from { transform: translate(110vw,20vh) rotate(0deg); }
    to { transform: translate(-10vw,80vh) rotate(360deg); }
}
</style>

<div class="light" style="left:20%;"></div>
<div class="light" style="left:60%; animation-duration:45s;"></div>
<div class="leaf">🍃</div>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SWITCH (INLINE ONLY)
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
# DATA
# ==================================================
if not os.path.exists(DAILY_FILE):
    pd.DataFrame(columns=["date","time","choice","note"]).to_csv(DAILY_FILE, index=False)

df = pd.read_csv(DAILY_FILE)

# ==================================================
# FLOW
# ==================================================
if st.session_state.page == "landing":
    st.markdown(f"## 💗 {T['title']}")
    st.markdown(T["landing"])
    if st.button(T["start"]):
        go("daily")

elif st.session_state.page == "daily":
    st.markdown(f"### {T['daily']}")
    st.markdown(T["story"])
    labels = [lbl for _, lbl in T["choices"]]
    keys = [k for k, _ in T["choices"]]
    idx = st.radio("", range(len(labels)), format_func=lambda i: labels[i])
    note = st.text_area(T["note"], height=180)
    if st.button(T["save"]):
        df.loc[len(df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            labels[idx],
            note
        ]
        df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"])
    if st.button("Close"):
        go("landing")
