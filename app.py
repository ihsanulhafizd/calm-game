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

def go(p):
    st.session_state.page = p

# ==================================================
# DATE
# ==================================================
now = datetime.now()
weekday = now.strftime("%A")
today_str = now.strftime("%d %B")

# ==================================================
# LONG DAILY MESSAGES (EN)
# ==================================================
DAILY_EN = {
    "Monday": (
        "It’s the beginning of a new week, my love.\n\n"
        "You don’t have to face everything at once. "
        "This day doesn’t demand strength or certainty from you.\n\n"
        "Take one breath. Then another.\n"
        "I’m here beside you, even in the quiet moments."
    ),
    "Tuesday": (
        "Today doesn’t need to be productive to be meaningful.\n\n"
        "If all you can do is exist and get through the hours, "
        "that is already enough.\n\n"
        "You are not behind. You are not failing.\n"
        "You are human — and deeply cared for."
    ),
    "Wednesday": (
        "The middle of the week can feel heavy.\n\n"
        "If your energy feels scattered or tired, that’s okay.\n"
        "You don’t need to push yourself past what feels safe.\n\n"
        "Rest when you need to.\n"
        "I’m still right here with you."
    ),
    "Thursday": (
        "You’ve already made it this far.\n\n"
        "Not because you were strong every moment, "
        "but because you kept going in your own quiet way.\n\n"
        "Even gentle steps count.\n"
        "Even pauses matter."
    ),
    "Friday": (
        "This week may have asked more from you than it should have.\n\n"
        "If you feel tired, overwhelmed, or unsure — you’re not wrong.\n\n"
        "Be kind to yourself tonight.\n"
        "You deserve softness and rest."
    ),
    "Saturday": (
        "Today doesn’t need plans or goals.\n\n"
        "You are allowed to move slowly, to do less, "
        "or to do nothing at all.\n\n"
        "Rest is not wasted time.\n"
        "It’s part of healing."
    ),
    "Sunday": (
        "As this week comes to an end, take a moment to breathe.\n\n"
        "Whatever didn’t get done can wait.\n"
        "Whatever feels heavy doesn’t have to be solved tonight.\n\n"
        "You don’t face tomorrow alone.\n"
        "I’ll still be here."
    )
}

# ==================================================
# LONG DAILY MESSAGES (ID)
# ==================================================
DAILY_ID = {
    "Monday": (
        "Awal minggu sering terasa berat, sayang.\n\n"
        "Kamu tidak harus menghadapi semuanya sekaligus hari ini.\n"
        "Hari ini tidak menuntut kamu untuk kuat atau sempurna.\n\n"
        "Tarik napas pelan.\n"
        "Aku ada di sampingmu."
    ),
    "Tuesday": (
        "Hari ini tidak harus produktif agar berarti.\n\n"
        "Jika yang bisa kamu lakukan hanya bertahan dan menjalani hari,\n"
        "itu sudah cukup.\n\n"
        "Kamu tidak tertinggal.\n"
        "Kamu tidak gagal.\n"
        "Kamu dicintai."
    ),
    "Wednesday": (
        "Pertengahan minggu sering melelahkan.\n\n"
        "Jika energimu terasa habis atau pikiranmu penuh,\n"
        "itu tidak apa-apa.\n\n"
        "Beristirahatlah jika perlu.\n"
        "Aku tetap di sini."
    ),
    "Thursday": (
        "Kamu sudah sampai sejauh ini.\n\n"
        "Bukan karena kamu selalu kuat,\n"
        "tapi karena kamu terus melangkah dengan caramu sendiri.\n\n"
        "Langkah kecil pun berarti.\n"
        "Berhenti sejenak pun sah."
    ),
    "Friday": (
        "Minggu ini mungkin terlalu banyak meminta darimu.\n\n"
        "Jika kamu lelah atau bingung, itu wajar.\n\n"
        "Bersikaplah lembut pada dirimu malam ini.\n"
        "Kamu pantas beristirahat."
    ),
    "Saturday": (
        "Hari ini tidak perlu rencana atau target.\n\n"
        "Kamu boleh berjalan pelan,\n"
        "melakukan sedikit,\n"
        "atau tidak melakukan apa-apa.\n\n"
        "Istirahat bukan kemunduran.\n"
        "Itu bagian dari pulih."
    ),
    "Sunday": (
        "Saat minggu ini berakhir, izinkan dirimu bernapas.\n\n"
        "Apa pun yang belum selesai bisa menunggu.\n"
        "Apa pun yang berat tidak harus diselesaikan malam ini.\n\n"
        "Kamu tidak sendirian menghadapi besok.\n"
        "Aku tetap di sini."
    )
}

# 🎉 Birthday (long & special)
BIRTHDAY_EN = (
    "🎉 Happy Birthday, my love.\n\n"
    "Today is not just another day.\n"
    "It’s the day the world quietly became warmer because you arrived.\n\n"
    "You don’t need to be strong today.\n"
    "You don’t need to carry anything.\n\n"
    "Let today hold you instead.\n\n"
    "You are deeply loved, just as you are.\n"
    "And I am endlessly grateful for you."
)

BIRTHDAY_ID = (
    "🎉 Selamat ulang tahun, sayang.\n\n"
    "Hari ini bukan hari biasa.\n"
    "Ini hari ketika dunia menjadi sedikit lebih hangat karena kamu ada.\n\n"
    "Hari ini kamu tidak perlu kuat.\n"
    "Tidak perlu menanggung apa pun.\n\n"
    "Biarkan hari ini yang memelukmu.\n\n"
    "Kamu sangat dicintai,\n"
    "apa adanya.\n"
    "Dan aku sangat bersyukur kamu ada."
)

# ==================================================
# TEXT MAP
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": (
            "My love,\n\n"
            "This space was made for days like this.\n\n"
            "Days when things feel heavy.\n"
            "Days when you don’t know what you’re feeling.\n\n"
            "There is nothing you need to fix here.\n"
            "Nothing you need to explain.\n\n"
            "Just take a moment.\n"
            "I’m here with you."
        ),
        "start": "Come in",
        "daily": "How does today feel?",
        "msg": BIRTHDAY_EN if today_str == "27 February" else DAILY_EN.get(weekday, ""),
        "choices": [
            "I took my sleep medication",
            "I delayed or reduced it",
            "I didn’t need it",
            "Today felt heavy, I rested"
        ],
        "note": "If you want, you can write what’s on your mind:",
        "save": "Save",
        "thanks": (
            "Thank you for taking this moment.\n\n"
            "Whatever you shared here matters.\n"
            "Whatever you chose is valid.\n\n"
            "I’m proud of you for showing up today.\n"
            "Rest now."
        )
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": (
            "Sayang,\n\n"
            "Ruang ini dibuat untuk hari-hari seperti ini.\n\n"
            "Hari ketika segalanya terasa berat.\n"
            "Hari ketika kamu tidak tahu harus merasa apa.\n\n"
            "Tidak ada yang perlu kamu perbaiki di sini.\n"
            "Tidak ada yang perlu kamu jelaskan.\n\n"
            "Ambil waktu sejenak.\n"
            "Aku di sini bersamamu."
        ),
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "msg": BIRTHDAY_ID if today_str == "27 February" else DAILY_ID.get(weekday, ""),
        "choices": [
            "Aku minum obat tidur",
            "Aku menunda atau mengurangi",
            "Aku tidak membutuhkannya",
            "Hari ini terasa berat, aku beristirahat"
        ],
        "note": "Kalau mau, tuliskan apa yang kamu rasakan:",
        "save": "Simpan",
        "thanks": (
            "Terima kasih sudah mengambil waktu ini.\n\n"
            "Apa pun yang kamu tuliskan berarti.\n"
            "Apa pun pilihanmu valid.\n\n"
            "Aku bangga kamu mau hadir hari ini.\n"
            "Istirahatlah."
        )
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (KEEP PREVIOUS VISUAL)
# ==================================================
st.markdown("""
<style>
.block-container { max-width: 620px; padding-top: 1.4rem; }
p { line-height: 1.75; }
</style>
""", unsafe_allow_html=True)

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
    st.markdown(T["msg"])
    choice = st.radio("", T["choices"])
    note = st.text_area(T["note"], height=120)
    if st.button(T["save"]):
        df.loc[len(df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            choice,
            note
        ]
        df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"])
    if st.button("OK"):
        go("landing")
