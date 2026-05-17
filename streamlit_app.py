import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests
from streamlit_lottie import st_lottie

# 1. PENGATURAN HALAMAN
st.set_page_config(
    page_title="B3 Waste Tracker Pro",
    page_icon="☣️",
    layout="wide"
)

# 2. FUNGSI MEMUAT ANIMASI LOTTIE
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Mengambil animasi bertema industri/lingkungan dari LottieFiles
lottie_factory = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_v7v9sc6n.json") 
# Jika url di atas tidak aktif, bisa gunakan alternatif animasi "loading/dashboard" umum:
if not lottie_factory:
    lottie_factory = load_lottieurl("https://lottie.host/549c44db-e204-4bda-be9f-86f37efbe065/wP8pMWeE6A.json")

# 3. DATABASE SIMBOL BAHAYA & KARAKTERISTIK LIMBAH
# Memetakan jenis limbah ke Simbol/Piktogram standar GHS/KLHK
B3_DATABASE = {
    "Sludge IPAL / Elektroplating": {"simbol": "☣️ Beracun (Toxic)", "warna": "red", "masa_simpan": 90},
    "Oli Bekas / Solvent": {"simbol": "🔥 Mudah Menyala (Flammable)", "warna": "orange", "masa_simpan": 180},
    "Aki Bekas / Asam-Asaman": {"simbol": "🧪 Korosif (Corrosive)", "warna": "purple", "masa_simpan": 365},
    "Kain Majun Terkontaminasi": {"simbol": "⚠️ Bahaya Terhadap Kesehatan", "warna": "blue", "masa_simpan": 180},
    "Fly Ash / Bottom Ash": {"simbol": "☣️ Beracun (Toxic)", "warna": "red", "masa_simpan": 365}
}

# 4. INITIALIZATION SESSION STATE (Simulasi Database di Memori)
if "b3_db" not in st.session_state:
    st.session_state.b3_db = pd.DataFrame(columns=[
        "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
        "Jenis Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
    ])

# 5. HEADER APLIKASI WITH LOTTIE ANIMATION
col_title, col_anim = st.columns([2, 1])
with col_title:
    st.title("☣️ Industrial Hazardous Waste Tracker")
    st.subheader("Sistem Manajemen & Kepatuhan Penyimpanan Limbah B3 di TPS")
    st.write("Aplikasi untuk memantau masa simpan, jenis wadah, dan simbol bahaya limbah B3 sesuai regulasi.")

with col_anim:
    if lottie_factory:
        st_lottie(lottie_factory, height=150, key="factory_anim")

st.markdown("---")

# 6. SIDEBAR: INPUT DATA LIMBAH BARU
st.sidebar.header("📥 Input Limbah Masuk TPS")
with st.sidebar.form(key="form_input_b3", clear_on_submit=True):
    jenis_limbah = st.selectbox("Pilih Jenis Limbah B3", list(B3_DATABASE.keys()))
    
    # Menampilkan info piktogram otomatis di sidebar saat memilih jenis limbah
    info_simbol = B3_DATABASE[jenis_limbah]["simbol"]
    st.info(f"Simbol Bahaya otomatis: {info_simbol}")
    
    # Fitur Baru: Jenis Wadah
    jenis_wadah = st.selectbox("Jenis Wadah / Kemasan", [
        "Drum Baja (Steel Drum)", 
        "Drum Plastik (HDPE Drum)", 
        "IBC Tank (1000 Liter)", 
        "Jumbo Bag", 
        "Box Container Plastic"
    ])
    
    berat = st.number_input("Berat Limbah (Kg)", min_value=1.0, step=10.0)
    tgl_masuk = st.date_input("Tanggal Masuk TPS", date.today())
    
    submit_btn = st.form_submit_button(label="Simpan ke TPS")

# Logika ketika tombol simpan ditekan
if submit_btn:
    # Hitung logika masa simpan
    id_limbah = f"B3-{datetime.now().strftime('%M%S')}"
    batas_hari = B3_DATABASE[jenis_limbah]["masa_simpan"]
    sisa_hari = batas_hari - (date.today() - tgl_masuk).days
    
    status = "Aman"
    if sisa_hari <= 14:
        status = "KRITIS 🔴"
    elif sisa_hari <= 30:
        status = "Peringatan 🟡"

    # Data baru dalam bentuk DataFrame
    new_data = pd.DataFrame([{
        "ID Limbah": id_limbah,
        "Jenis Limbah": jenis_limbah,
        "Karakteristik / Simbol": info_simbol,
        "Jenis Wadah": jenis_wadah,
        "Berat (Kg)": berat,
        "Tanggal Masuk": tgl_masuk,
        "Batas Hari": f"{batas_hari} Hari",
        "Sisa Hari": sisa_hari,
        "Status": status
    }])
    
    # Gabungkan ke database utama
    st.session_state.b3_db = pd.concat([st.session_state.b3_db, new_data], ignore_index=True)
    st.success(f"Berhasil menambahkan {jenis_limbah} ke TPS!")

# 7. HALAMAN UTAMA: DASBOR MONITORING
st.header("📊 Dasbor Real-Time TPS Limbah B3")

if st.session_state.b3_db.empty:
    st.info("Belum ada data limbah di TPS. Silakan menginput data melalui menu di sidebar kiri.")
else:
    # Hitung Ringkasan Metrik
    total_berat = st.session_state.b3_db["Berat (Kg)"].sum()
    total_item = len(st.session_state.b3_db)
    item_kritis = len(st.session_state.b3_db[st.session_state.b3_db["Sisa Hari"] <= 14])

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Massa di TPS", f"{total_berat:,.0f} Kg", "Kapasitas Maks: 10 Ton")
    col_m2.metric("Jumlah Wadah/Lot Aktif", f"{total_item} Lot")
    col_m3.metric("Lot Status Kritis (<14 Hari)", f"{item_kritis} Lot", delta="- Tindakan Segera" if item_kritis > 0 else "Aman", delta_color="inverse")

    st.markdown("### 📜 Tabel Inventaris Aktif")
    
    # Fungsi mewarnai baris berdasarkan tingkat kekritisan sisa hari penyimpanan
    def color_status(val):
        if "KRITIS" in str(val):
            return "background-color: #ffcccc; color: black; font-weight: bold;"
        elif "Peringatan" in str(val):
            return "background-color: #fff2cc; color: black;"
        return "background-color: #e2f0d9; color: black;"

    # Menampilkan dataframe dengan styling warna otomatis pada kolom Status
    df_styled = st.session_state.b3_db.style.applymap(color_status, subset=["Status"])
    
    st.dataframe(df_styled, use_container_width=True)

    # Fitur Tambahan: Tombol Clear untuk Simulasi Ulang
    if st.button("Kosongkan Data TPS (Reset)"):
        st.session_state.b3_db = pd.DataFrame(columns=[
            "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
            "Jenis Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
        ])
        st.rerun()
