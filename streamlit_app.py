import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import io

# 1. Konfigurasi Halaman (Adaptif/Wide Mode)
st.set_page_config(
    page_title="Sistem Informasi Indeks Kualitas Air",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Fungsi Pendukung
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Konversi DataFrame ke Excel/CSV untuk fitur Download
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Memuat animasi Lottie
lottie_water_clean = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_R89V70.json") # Animasi air bersih
lottie_water_polluted = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_go76w8ga.json") # Animasi peringatan

# 3. Sidebar - Navigasi Menu
st.sidebar.title("🌊 Navigasi IKA")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "📊 Aplikasi Utama (Input Data)", "ℹ️ Tentang & Unduh Data"]
)

# Dummy Data Global (Bisa diunduh di menu "Tentang")
data_historis = pd.DataFrame({
    "Tanggal": pd.date_range(start="2026-05-01", periods=5, freq='D').strftime('%Y-%m-%d'),
    "pH": [7.2, 6.8, 5.5, 7.0, 8.2],
    "DO (mg/L)": [6.5, 5.8, 3.2, 6.1, 4.0],
    "BOD (mg/L)": [2.1, 2.8, 6.5, 2.9, 4.2],
    "TSS (mg/L)": [15, 22, 65, 18, 55],
    "Status": ["Baik", "Baik", "Tercemar", "Baik", "Tercemar Ringan"]
})


# ==================== HALAMAN 1: BERANDA ====================
if menu == "🏠 Beranda":
    st.title("🏠 Sistem Informasi Indeks Kualitas Air (IKA)")
    st.subheader("Selamat Datang di Platform Monitoring Lingkungan")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Apa itu Indeks Kualitas Air (IKA)?
        Indeks Kualitas Air adalah parameter nilai tunggal yang digunakan untuk menentukan tingkat kekompakan atau kondisi kualitas air di suatu sumber air (sungai, danau, atau laut) dalam kurun waktu tertentu. 
        
        Platform ini dirancang secara **adaptif** untuk membantu akademisi, praktisi industri, maupun instansi lingkungan dalam memonitor kelayakan air baku secara cepat berdasarkan baku mutu yang berlaku di Indonesia (seperti **PP No. 22 Tahun 2021**).
        
        ### Fitur Utama Aplikasi:
        *   **Analisis Real-time:** Input parameter kimia-fisika air langsung via slider eksternal.
        *   **Visualisasi Adaptif:** Desain layout yang fleksibel untuk berbagai ukuran layar monitor maupun smartphone.
        *   **Indikator Animasi Interaktif:** Integrasi animasi Lottie untuk memberikan respon visual langsung terhadap status pencemaran air.
        *   **Ekspor Data:** Fitur pengunduhan data hasil uji laboratorium.
        """)
    with col2:
        if lottie_water_clean:
            st_lottie(lottie_water_clean, height=300, key="beranda_anim")


# ==================== HALAMAN 2: APLIKASI UTAMA ====================
elif menu == "📊 Aplikasi Utama (Input Data)":
    st.title("📊 Analisis Real-Time Kualitas Air")
    st.write("Silakan atur parameter air pada bilah geser (*slider*) di bawah ini untuk melihat hasil analisis.")
    st.markdown("---")
    
    # Input parameter diletakkan di body utama agar halaman adaptif, terbagi dalam 4 kolom kecil
    st.markdown("#### 🔧 Pengaturan Parameter Uji")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        ph = st.slider("Derajat Keasaman (pH)", 0.0, 14.0, 7.0, 0.1)
    with p_col2:
        do = st.slider("DO (Dissolved Oxygen) - mg/L", 0.0, 15.0, 6.5, 0.1)
    with p_col3:
        bod = st.slider("BOD - mg/L", 0.0, 20.0, 3.0, 0.1)
    with p_col4:
        tss = st.slider("TSS - mg/L", 0.0, 100.0, 20.0, 1.0)
        
    st.markdown("---")

    # Logika Penentuan Status (Simulasi sederhana Baku Mutu Air Kelas II)
    if 6.0 <= ph <= 9.0 and do >= 4.0 and bod <= 3.0 and tss <= 50:
        status = "BAIK (Memenuhi Baku Mutu PP 22/2021 Kelas II)"
        alert_type = "success"
        animasi_aktif = lottie_water_clean
    else:
        status = "TERCEMAR / MELEBIHI BAKU MUTU"
        alert_type = "warning"
        animasi_aktif = lottie_water_polluted

    # Menampilkan Layout Hasil (2 Kolom Adaptif)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Ringkasan Parameter Terinput")
        metric_1, metric_2 = st.columns(2)
        with metric_1:
            st.metric(label="pH Terukur", value=ph)
            st.metric(label="DO Air", value=f"{do} mg/L")
        with metric_2:
            st.metric(label="BOD Air", value=f"{bod} mg/L")
            st.metric(label="TSS Air", value=f"{tss} mg/L")
            
        st.markdown("### 📢 Hasil Keputusan")
        if alert_type == "success":
            st.success(f"**Status Air: {status}**")
        else:
            st.warning(f"**Status Air: {status}**")

    with col2:
        st.markdown("### ⚡ Indikator Visual Lottie")
        if animasi_aktif:
            st_lottie(animasi_aktif, height=300, key="main_anim")
        else:
            st.info("Memuat animasi...")


# ==================== HALAMAN 3: TENTANG & UNDUH DATA ====================
elif menu == "ℹ️ Tentang & Unduh Data":
    st.title("ℹ️ Informasi Pengembang & Repositori Data")
    st.markdown("---")
    
    # Bagian 1: Tentang Pembuat Web (Gunakan format kartu profil sederhana)
    st.markdown("### 👤 Profil Pengembang")
    col_foto, col_bio = st.columns([1, 3])
    with col_foto:
        # Placeholder lingkaran emoji atau gambar instansi Anda
        st.header("💧🔬")
    with col_bio:
        st.markdown("""
        *   **Nama Pengembang / Tim**: Tim Rekayasa Lingkungan & IT
        *   **Fokus Bidang**: *Environmental Engineering / Industrial Chemistry / Occupational Health and Safety (K3)*
        *   **Tujuan Proyek**: Mempermudah pemantauan kualitas air limbah industri maupun badan air domestik menggunakan integrasi web mutakhir yang responsif.
        """)
        
    st.markdown("---")
    
    # Bagian 2: Tabel Data dan Fitur Unduh (Download) Data
    st.markdown("### 💾 Pusat Data Historis")
    st.write("Di bawah ini merupakan contoh log data pemantauan berkala yang tersimpan di sistem. Anda dapat mengunduhnya dalam format CSV.")
    
    # Tampilkan tabel secara adaptif penuh
    st.dataframe(data_historis, use_container_width=True)
    
    # Tombol download data
    csv_data = convert_df_to_csv(data_historis)
    
    st.download_button(
        label="📥 Unduh Data Kualitas Air (.CSV)",
        data=csv_data,
        file_name="data_historis_kualitas_air.csv",
        mime="text/csv",
    )
    st.caption("Klik tombol di atas untuk menyimpan spreadsheet ke perangkat Anda.")
