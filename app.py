import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =====================
# KONFIGURASI DASAR
# =====================
PLAYER_NAME = "Zara"   # ganti ke "Sayang" jika mau
DATA_FILE = "data.csv"

st.set_page_config(
    page_title="🌱 Calm Game",
    page_icon="🌙",
    layout="centered"
)

# =====================
# LOAD / INIT DATA
# =====================
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["tanggal", "poin"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

# =====================
# PILIH MODE
# =====================
mode = st.sidebar.selectbox(
    "Mode",
    ["🎮 Player", "👀 Viewer"]
)

# =====================
# PLAYER MODE
# =====================
if mode == "🎮 Player":
    st.title(f"🌱 Calm Game untuk {PLAYER_NAME}")
    st.caption("Setiap langkah kecil itu berarti 💚")

    st.markdown("### 📝 Daily Check-in")

    jujur = st.checkbox("Aku jujur hari ini")
    tunda = st.checkbox("Aku menunda obat")
    alternatif = st.checkbox("Aku mencoba cara lain")
    tenang = st.checkbox("Tidur terasa lebih tenang")
    ngobrol = st.checkbox("Aku mau ngobrol")
    hari_berat = st.checkbox("Hari ini terasa berat")

    poin = 0
    if jujur: poin += 2
    if tunda: poin += 1
    if alternatif: poin += 1
    if tenang: poin += 1
    if ngobrol: poin += 2
    if hari_berat: poin -= 1
    if poin < 0: poin = 0

    if poin < 10:
        level = "🌱 Seedling"
        pesan = "Pelan-pelan itu tidak apa-apa."
    elif poin < 20:
        level = "🌿 Growing"
        pesan = "Progres kamu konsisten."
    elif poin < 30:
        level = "☀️ Stable"
        pesan = "Kamu semakin stabil."
    else:
        level = "🌟 Strong"
        pesan = "Kamu luar biasa."

    if st.button("✨ Selesai Hari Ini"):
        today = datetime.now().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([[today, poin]], columns=["tanggal", "poin"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success(f"Terima kasih sudah berusaha hari ini, {PLAYER_NAME} 🌱")
        st.progress(min(poin / 30, 1.0))
        st.markdown(f"**Level:** {level}")
        st.caption(pesan)

# =====================
# VIEWER MODE
# =====================
if mode == "👀 Viewer":
    st.title("👀 Progress Overview")

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.dataframe(df)

        total = df["poin"].sum()
        st.metric("Total Poin", total)

        st.line_chart(df.set_index("tanggal")["poin"])
