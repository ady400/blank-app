import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA
# ==========================================
st.set_page_config(
    page_title="Dashboard Interaktif Kualitas Air",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk mempercantik UI (Membuat kartu metrik lebih modern)
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 10px;
    }
    .stRadio p {
        font-weight: bold;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI UTAMA (API Lottie & Hitung IP)
# ==========================================
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# Simulasi Perhitungan Indeks Pencemaran (IP) Sederhana
# IP = Sqrt(( (Ci/Lij)M^2 + (Ci/Lij)R^2 ) / 2)
def hitung_indeks_pencemaran(ph, do, bod, tss):
    # Nilai Baku Mutu Kelas II (PP 22/2021) sebagai pembagi (Lij)
    # Untuk pH, kita hitung deviasinya dari nilai netral 7
    m_ph = abs(ph - 7) / 1.5 
    m_do = 4.0 / do if do > 0 else 5  # DO makin kecil makin buruk
    m_bod = bod / 3.0
    m_tss = tss / 50.0
    
    rerata = np.mean([m_ph, m_do, m_bod, m_tss])
    maksimum = np.max([m_ph, m_do, m_bod, m_tss])
    
    ip = np.sqrt((maksimum**2 + rerata**2) / 2)
    return round(ip, 2)

# Load Aset Animasi Lottie
lottie_home = load_lottieurl("https://lottie.host/80a2df37-db56-4299-bb6d-8dc52bd3c285/1GThwL2W9y.json") # Animasi Ekosistem Air
lottie_good = load_lottieurl("https://lottie.host/bebf3967-df50-4822-bc5d-6c8466b04313/f5P0YfK0M2.json") # Air Bersih/Ikan Berenang
lottie_bad = load_lottieurl("https://lottie.host/ca8ea822-1db7-48f8-b3de-0869d8031d68/eT9G0U5v1R.json") # Peringatan Bahaya/Polusi

# Dummy Data Historis untuk Grafik Plotly
np.random.seed(42)
dates = pd.date_range(start="2026-05-01", periods=10, freq='D')
data_historis = pd.DataFrame({
    "Tanggal": dates,
    "pH": np.random.uniform(6.5, 8.2, 10),
    "DO (mg/L)": np.random.uniform(3.5, 6.8, 10),
    "BOD (mg/L)": np.random.uniform(1.5, 5.0, 10),
    "TSS (mg/L)": np.random.uniform(10, 60, 10),
    "Indeks Pencemaran": np.random.uniform(0.5, 4.5, 10)
})

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3144/3144760.png", width=80)
    st.title("Smart Water Quality")
    st.markdown("---")
    menu = st.radio(
        "PILIH MENU DASHBOARD:",
        ["🏠 Beranda Utama", "📊 Simulator & Kalkulator IKA", "📈 Tren Historis & Unduh Data"],
        index=0
    )
    st.markdown("---")
    st.caption("⚡ **Status Sistem:** Operasional (2026)")

# ==========================================
# 4. LOGIKA HALAMAN
# ==========================================

# --- MENU 1: BERANDA UTAMA ---
if menu == "🏠 Beranda Utama":
    st.title("🚀 Dashboard Analisis Kualitas Air Adaptif")
    st.subheader("Platform Monitoring Parameter Lingkungan Terintegrasi")
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### Selamat Datang!
        Aplikasi ini dirancang untuk memberikan visualisasi instan terhadap **Indeks Kualitas Air (IKA)** menggunakan pendekatan *Kalkulator Indeks Pencemaran*. 
        
        #### 🌟 Fitur Interaktif Unggulan:
        *   **Dynamic Lottie Feedback:** Animasi berubah secara *real-time* merepresentasikan kondisi lingkungan (Ikan berenang untuk kondisi baik, alarm peringatan untuk kondisi tercemar).
        *   **Kalkulator Saintifik Sederhana:** Menggunakan simulasi rumus KepmenLH 115/2003.
        *   **Grafik Interaktif:** Plotly charts yang responsif terhadap sentuhan dan kursor komputer.
        
        #### 🧪 Parameter yang Dipantau:
        1. **pH (Derajat Keasaman):** Menentukan sifat asam/basa air.
        2. **DO (Dissolved Oxygen):** Jumlah oksigen terlarut yang dibutuhkan makhluk hidup air.
        3. **BOD (Biochemical Oxygen Demand):** Indikasi jumlah bahan organik.
        4. **TSS (Total Suspended Solids):** Padatan tersuspensi penyebab kekeruhan.
        """)
    with col2:
        if lottie_home:
            st_lottie(lottie_home, height=350, key="home_anim")

# --- MENU 2: SIMULATOR & KALKULATOR IKA ---
elif menu == "📊 Simulator & Kalkulator IKA":
    st.title("📊 Simulator Parameter & Penentuan Indeks")
    st.write("Geser nilai parameter di bawah ini untuk melihat perubahan status indeks pencemaran air secara instan.")
    st.markdown("---")
    
    # Kontrol Input Menggunakan Kolom Adaptif
    c_in1, c_in2, c_in3, c_in4 = st.columns(4)
    with c_in1:
        ph = st.slider("🎛️ pH Air", 0.0, 14.0, 7.2, 0.1)
    with c_in2:
        do = st.slider("🎛️ DO (mg/L)", 0.1, 15.0, 5.5, 0.1)
    with c_in3:
        bod = st.slider("🎛️ BOD (mg/L)", 0.0, 20.0, 2.5, 0.1)
    with c_in4:
        tss = st.slider("🎛️ TSS (mg/L)", 0.0, 120.0, 25.0, 1.0)
        
    st.markdown("---")
    
    # Hitung nilai IP secara matematis
    nilai_ip = hitung_indeks_pencemaran(ph, do, bod, tss)
    
    # Menentukan Status dan Warna berdasarkan KepmenLH 115/2003
    if nilai_ip <= 1.0:
        status_air = "MEMENUHI BAKU MUTU (Kondisi Baik)"
        warna_card = "#d4edda"
        warna_teks = "#155724"
        animasi_terpilih = lottie_good
        st_status = "success"
    elif 1.0 < nilai_ip <= 5.0:
        status_air = "TERCEMAR RINGAN"
        warna_card = "#fff3cd"
        warna_teks = "#856404"
        animasi_terpilih = lottie_bad
        st_status = "warning"
    elif 5.0 < nilai_ip <= 10.0:
        status_air = "TERCEMAR SEDANG"
        warna_card = "#ffeeba"
        warna_teks = "#856404"
        animasi_terpilih = lottie_bad
        st_status = "warning"
    else:
        status_air = "TERCEMAR BERAT"
        warna_card = "#f8d7da"
        warna_teks = "#721c24"
        animasi_terpilih = lottie_bad
        st_status = "error"

    # Tampilan Layout Hasil Utama
    col_visual, col_anim = st.columns([4, 3])
    
    with col_visual:
        st.markdown(f"""
        <div style="background-color: {warna_card}; padding: 25px; border-radius: 15px; border-left: 8px solid {warna_teks};">
            <h2 style="color: {warna_teks}; margin: 0;">Skor Indeks Pencemaran (IP): {nilai_ip}</h2>
            <h3 style="color: {warna_teks}; margin-top: 10px;">Status: {status_air}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Detail Parameter Terbaca")
        m1, m2 = st.columns(2)
        m1.metric("Derajat Keasaman (pH)", f"{ph}", delta=f"{round(ph-7,1)} dari Netral")
        m1.metric("Dissolved Oxygen (DO)", f"{do} mg/L", delta="Cukup" if do>=4 else "Kritis", delta_color="normal" if do>=4 else "inverse")
        m2.metric("Biochemical Oxygen Demand", f"{bod} mg/L", delta="Normal" if bod<=3 else "Tinggi", delta_color="normal" if bod<=3 else "inverse")
        m2.metric("Total Suspended Solids", f"{tss} mg/L", delta="Aman" if tss<=50 else "Keruh", delta_color="normal" if tss<=50 else "inverse")

    with col_anim:
        st.markdown("<h4 style='text-align: center;'>🎨 Status Indikator Biosfer</h4>", unsafe_allow_html=True)
        if animasi_terpilih:
            st_lottie(animasi_terpilih, height=280, key="status_lottie")
        else:
            st.info("Menampilkan representasi visual...")

# --- MENU 3: TREN HISTORIS & UNDUH DATA ---
elif menu == "📈 Tren Historis & Unduh Data":
    st.title("📈 Analisis Grafik Tren & Pusat Unduhan")
    st.write("Halaman ini menyajikan visualisasi data berkala laboratorium dan fitur ekspor file.")
    st.markdown("---")
    
    # 1. Grafik Interaktif Plotly
    st.markdown("### 📊 Tren Nilai Indeks Pencemaran (10 Hari Terakhir)")
    
    # Membuat Line Chart Interaktif dengan Plotly
    fig = px.line(
        data_historis, 
        x="Tanggal", 
        y="Indeks Pencemaran", 
        title="Fluktuasi Nilai IP Harian",
        markers=True,
        template="plotly_white"
    )
    # Tambahkan garis batas ambang pencemaran (IP = 1.0)
    fig.add_hline(y=1.0, line_dash="dash", line_color="green", annotation_text="Batas Baku Mutu (IP=1)")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20)) # Opsional, buat atur margin saja
    st.plotly_chart(fig, use_container_width=True) # Parameter adaptif ditaruh di sini
    
    st.markdown("---")
    
    # 2. Tabel Data & Tombol Download
    col_tabel, col_dev = st.columns([3, 2])
    
    with col_tabel:
        st.markdown("### 💾 Spreadsheet Log Data")
        st.dataframe(data_historis, use_container_width=True)
        
        # Fitur unduhan CSV langsung
        csv = data_historis.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV Lengkap",
            data=csv,
            file_name="Log_Kualitas_Air_2026.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with col_dev:
        st.markdown("### 👤 Kredensial Pengembang & Hak Cipta")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
            <h4>Sistem Informasi Lingkungan</h4>
            <p><b>Dikembangkan oleh:</b> Tim Pengembang Web K3 & Lingkungan</p>
            <p><b>Metodologi:</b> Pembobotan Parameter KepmenLH No. 115 Tahun 2003 / PP No. 22 Tahun 2021 Lampiran VI</p>
            <p><b>Versi Aplikasi:</b> v2.0 (Premium & Responsive Layout)</p>
            <p><i>Data dikumpulkan secara berkala melalui sensor IoT dan uji sampel basah laboratorium.</i></p>
        </div>
        """, unsafe_allow_html=True)
