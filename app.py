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
    if 0 <= h <= 0 or 4 <= h <= 5:
        return "deep_night"
    if 18 <= h <= 23:
        return "night"
    return "day"

PHASE = time_phase(hour)

# ==================================================
# BASE BOOK-STYLE MESSAGES
# ==================================================
BASE_EN = {
    "day": (
        "This day does not ask you to hurry.\n\n"
        "You are allowed to move gently through these hours, "
        "carrying only what feels possible.\n\n"
        "There is no race here.\n"
        "You are already enough."
    ),
    "night": (
        "The night has settled in.\n\n"
        "If your thoughts are louder now, you don’t need to quiet them.\n\n"
        "Let the day loosen its grip.\n"
        "I’m here with you in this calm."
    ),
    "deep_night": (
        "It’s late, and the world is mostly asleep.\n\n"
        "You don’t need answers in the dark.\n"
        "You don’t need to solve anything now.\n\n"
        "Just breathe.\n"
        "You’re not alone."
    ),
    "very_late_night": (
        "It’s very late now.\n\n"
        "If you’re still awake, that’s okay.\n"
        "Nothing is wrong with you.\n\n"
        "Wrap yourself in something soft.\n"
        "Even this moment is allowed to be gentle.\n\n"
        "I’m right here, keeping you company."
    )
}

BASE_ID = {
    "day": (
        "Hari ini tidak meminta kamu untuk bergegas.\n\n"
        "Kamu boleh menjalani jam-jam ini dengan pelan, "
        "membawa hanya yang sanggup kamu bawa.\n\n"
        "Tidak ada perlombaan di sini.\n"
        "Kamu sudah cukup."
    ),
    "night": (
        "Malam telah datang.\n\n"
        "Jika pikiranmu lebih ramai sekarang, "
        "kamu tidak perlu memaksanya diam.\n\n"
        "Biarkan hari ini melonggar.\n"
        "Aku di sini bersamamu."
    ),
    "deep_night": (
        "Sudah larut, dan dunia hampir tertidur.\n\n"
        "Kamu tidak perlu jawaban dalam gelap.\n"
        "Tidak perlu menyelesaikan apa pun sekarang.\n\n"
        "Bernapaslah.\n"
        "Kamu tidak sendirian."
    ),
    "very_late_night": (
        "Sekarang sudah sangat larut.\n\n"
        "Jika kamu masih terjaga, itu tidak apa-apa.\n"
        "Tidak ada yang salah denganmu.\n\n"
        "Selimuti dirimu dengan sesuatu yang hangat.\n"
        "Bahkan momen ini boleh lembut.\n\n"
        "Aku di sini menemanimu."
    )
}

# 🎉 Birthday override
BIRTHDAY_EN = (
    "🎉 *Happy Birthday, my love.*\n\n"
    "*Today is not for carrying weight.*\n\n"
    "*Let today hold you instead.*\n\n"
    "*You are deeply loved — exactly as you are.*"
)
BIRTHDAY_ID = (
    "🎉 *Selamat ulang tahun, sayang.*\n\n"
    "*Hari ini bukan untuk menanggung beban.*\n\n"
    "*Biarkan hari ini yang memelukmu.*\n\n"
    "*Kamu sangat dicintai — apa adanya.*"
)

# ==================================================
# CHOICE-AWARE THANK YOU MESSAGES
# ==================================================
THANKS_BY_CHOICE_EN = {
    "med": {
        "day": (
            "Thank you for being honest with yourself.\n\n"
            "Taking medication does not erase your effort.\n"
            "It means you chose care in the way you could today.\n\n"
            "Be gentle with yourself."
        ),
        "night": (
            "Tonight, choosing support was an act of care.\n\n"
            "You did not give up.\n"
            "You listened to your limits.\n\n"
            "Rest softly."
        ),
        "deep_night": (
            "At this hour, survival matters more than perfection.\n\n"
            "You chose what helped you stay afloat.\n"
            "That is enough for now."
        ),
        "very_late_night": (
            "So late at night, even small choices take courage.\n\n"
            "You chose care.\n"
            "Let yourself be held by rest."
        )
    },
    "delay": {
        "day": (
            "You tried to pause, even briefly.\n\n"
            "That space you created matters.\n"
            "Progress can be quiet."
        ),
        "night": (
            "Tonight, you listened before reacting.\n\n"
            "That awareness is not small.\n"
            "I’m proud of you."
        ),
        "deep_night": (
            "Even in the dark, you made room for choice.\n\n"
            "That counts.\n"
            "Rest now."
        ),
        "very_late_night": (
            "At this hour, restraint is tiring.\n\n"
            "You did what you could.\n"
            "That is enough."
        )
    },
    "none": {
        "day": (
            "Today, your body carried you on its own.\n\n"
            "Notice that strength — quietly.\n"
            "You earned this gentleness."
        ),
        "night": (
            "Tonight, you didn’t need extra support.\n\n"
            "That doesn’t mean tomorrow must be the same.\n"
            "For now, rest."
        ),
        "deep_night": (
            "Being awake without needing medication can feel strange.\n\n"
            "Let your body find its rhythm.\n"
            "You’re safe."
        ),
        "very_late_night": (
            "So late, and you’re still here.\n\n"
            "Nothing to prove.\n"
            "Just breathe."
        )
    },
    "rest": {
        "day": (
            "Choosing rest is not avoidance.\n\n"
            "It is wisdom.\n"
            "Your body asked, and you listened."
        ),
        "night": (
            "Tonight felt heavy, and you honored that.\n\n"
            "Rest is a response, not a failure."
        ),
        "deep_night": (
            "At this hour, resting is an act of kindness.\n\n"
            "Let yourself sink into it."
        ),
        "very_late_night": (
            "So late, heaviness can feel louder.\n\n"
            "You chose to rest.\n"
            "That was the right thing."
        )
    }
}

THANKS_BY_CHOICE_ID = {
    "med": {
        "day": (
            "Terima kasih sudah jujur pada dirimu.\n\n"
            "Minum obat tidak menghapus usahamu.\n"
            "Itu berarti kamu memilih merawat diri hari ini."
        ),
        "night": (
            "Malam ini, memilih bantuan adalah bentuk peduli.\n\n"
            "Kamu tidak menyerah.\n"
            "Istirahatlah dengan lembut."
        ),
        "deep_night": (
            "Di jam ini, bertahan lebih penting dari sempurna.\n\n"
            "Pilihanmu sudah cukup."
        ),
        "very_late_night": (
            "Di jam yang sangat larut, pilihan kecil pun butuh tenaga.\n\n"
            "Kamu memilih merawat diri.\n"
            "Biarkan dirimu beristirahat."
        )
    },
    "delay": {
        "day": (
            "Kamu mencoba memberi jeda.\n\n"
            "Ruang kecil itu berarti.\n"
            "Perubahan bisa sunyi."
        ),
        "night": (
            "Malam ini, kamu mendengarkan dirimu dulu.\n\n"
            "Aku bangga padamu."
        ),
        "deep_night": (
            "Bahkan dalam gelap, kamu memberi ruang untuk memilih.\n\n"
            "Istirahatlah."
        ),
        "very_late_night": (
            "Menahan diri di jam ini melelahkan.\n\n"
            "Apa yang kamu lakukan sudah cukup."
        )
    },
    "none": {
        "day": (
            "Hari ini tubuhmu menopangmu sendiri.\n\n"
            "Sadari kekuatan itu — dengan lembut."
        ),
        "night": (
            "Malam ini kamu tidak membutuhkan tambahan.\n\n"
            "Besok tidak harus sama.\n"
            "Untuk sekarang, beristirahatlah."
        ),
        "deep_night": (
            "Terjaga tanpa obat bisa terasa aneh.\n\n"
            "Biarkan tubuh menemukan ritmenya.\n"
            "Kamu aman."
        ),
        "very_late_night": (
            "Sudah sangat larut, dan kamu masih di sini.\n\n"
            "Tidak perlu membuktikan apa pun.\n"
            "Bernapaslah."
        )
    },
    "rest": {
        "day": (
            "Memilih istirahat bukan menghindar.\n\n"
            "Itu kebijaksanaan.\n"
            "Tubuhmu meminta, dan kamu mendengar."
        ),
        "night": (
            "Malam ini terasa berat, dan kamu menghormatinya.\n\n"
            "Istirahat bukan kegagalan."
        ),
        "deep_night": (
            "Di jam ini, istirahat adalah kebaikan.\n\n"
            "Biarkan dirimu tenggelam di dalamnya."
        ),
        "very_late_night": (
            "Di jam yang sangat larut, berat terasa lebih keras.\n\n"
            "Kamu memilih istirahat.\n"
            "Itu tepat."
        )
    }
}

# ==================================================
# TEXT MAP
# ==================================================
TEXT = {
    "en": {
        "title": APP_TITLE_EN,
        "landing": (
            "*This space is not asking you to change.*\n\n"
            "*It is here to walk with you, page by page.*\n\n"
            "*Take your time.*"
        ),
        "start": "Enter",
        "daily": "How does today feel?",
        "base": BIRTHDAY_EN if today_str == "27 February" else BASE_EN[PHASE],
        "choices": [
            ("med", "I took my sleep medication"),
            ("delay", "I delayed or reduced it"),
            ("none", "I didn’t need it"),
            ("rest", "Today felt heavy, I rested")
        ],
        "note": "You can write anything you want here:",
        "save": "Save",
        "thanks": lambda key: (
            BIRTHDAY_EN if today_str == "27 February"
            else THANKS_BY_CHOICE_EN[key][PHASE]
        )
    },
    "id": {
        "title": APP_TITLE_ID,
        "landing": (
            "*Ruang ini tidak meminta kamu berubah.*\n\n"
            "*Ia berjalan bersamamu, halaman demi halaman.*\n\n"
            "*Ambil waktumu.*"
        ),
        "start": "Masuk",
        "daily": "Bagaimana hari ini terasa?",
        "base": BIRTHDAY_ID if today_str == "27 February" else BASE_ID[PHASE],
        "choices": [
            ("med", "Aku minum obat tidur"),
            ("delay", "Aku menunda atau mengurangi"),
            ("none", "Aku tidak membutuhkannya"),
            ("rest", "Hari ini terasa berat, aku beristirahat")
        ],
        "note": "Kamu bisa menuliskan apa pun di sini:",
        "save": "Simpan",
        "thanks": lambda key: (
            BIRTHDAY_ID if today_str == "27 February"
            else THANKS_BY_CHOICE_ID[key][PHASE]
        )
    }
}

T = TEXT[st.session_state.lang]

# ==================================================
# STYLE (BOOK FEEL)
# ==================================================
st.markdown("""
<style>
.block-container { max-width: 640px; padding-top: 1.8rem; }
p { font-style: italic; line-height: 1.9; font-size: 16px; }
.lang { position: fixed; top: 12px; right: 18px; font-size: 11px; opacity: .8; }
.lang span { cursor: pointer; margin-left: 6px; }
.active { font-weight: 600; opacity: 1; }
.inactive { opacity: .5; }
</style>
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
    st.markdown(T["base"])
    labels = [lbl for _, lbl in T["choices"]]
    keys = [k for k, _ in T["choices"]]
    idx = st.radio("", range(len(labels)), format_func=lambda i: labels[i])
    choice_key = keys[idx]
    note = st.text_area(T["note"], height=160)
    if st.button(T["save"]):
        st.session_state.last_choice = choice_key
        df.loc[len(df)] = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            labels[idx],
            note
        ]
        df.to_csv(DAILY_FILE, index=False)
        go("thanks")

elif st.session_state.page == "thanks":
    st.markdown(T["thanks"](st.session_state.last_choice))
    if st.button("Close"):
        go("landing")
