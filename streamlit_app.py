import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA
# ==========================================
st.set_page_config(
    page_title="EcoWater COD Analyzer",
    page_icon="🌱",
    layout="centered",
)

# Database Riwayat Perhitungan
NAMA_FILE_HISTORY = "riwayat_cod.csv"

# Inisialisasi Database jika belum ada
if not os.path.exists(NAMA_FILE_HISTORY):
    df_init = pd.DataFrame(columns=["Waktu", "Petugas", "Sampel", "Baku Mutu", "Hasil (mg/L)", "Status", "Interpretasi"])
    df_init.to_csv(NAMA_FILE_HISTORY, index=False)

# Custom CSS Global (Tetap menjaga gaya Visual sebelumnya)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #f0fdf4 !important; }
    
    /* Center Elements */
    .stApp h1, .stApp h2, .stApp h3 { text-align: center !important; color: #047857; }
    [data-testid="stImage"] { display: flex; justify-content: center; }
    [data-testid="stImage"] img { border-radius: 15px; max-width: 80% !important; }

    /* Custom Card */
    .custom-card {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://i.pinimg.com/736x/a0/92/58/a09258df83907bc5d1f8f506a037cd76.jpg", width=100)
    st.markdown("<h2 style='text-align: center;'>EcoWater</h2>", unsafe_allow_html=True)
    menu = st.radio("Navigasi Halaman:", ["🏠 Beranda", "🧮 Kalkulator COD", "📜 Riwayat & Laporan", "ℹ️ Tentang"])
    st.markdown("---")
    st.success("Sistem Aktif 🟢")

# ==========================================
# 3. LOGIKA HALAMAN
# ==========================================

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.markdown("<h1>🌱 EcoWater COD Analyzer</h1>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/1200x/48/81/54/4881545ab4580b32e5bb0ce8679b8598.jpg", caption="Melindungi sumber daya air untuk masa depan hijau.")
    
    st.markdown("""
    <div class="custom-card">
        <h3>Selamat Datang</h3>
        <p>Aplikasi standar laboratorium untuk menghitung kadar <b>Chemical Oxygen Demand (COD)</b> secara otomatis, 
        lengkap dengan fitur manajemen logbook dan pelaporan digital sesuai regulasi LHK.</p>
    </div>
    """, unsafe_allow_html=True)

# --- HALAMAN KALKULATOR ---
elif menu == "🧮 Kalkulator COD":
    st.markdown("<h1>Kalkulator Kadar COD</h1>", unsafe_allow_html=True)
    
    with st.expander("📝 Rumus Perhitungan (Metode Titrimetri)"):
        st.latex(r"COD (mg/L) = \frac{(A - B) \times N \times 8000}{V_{sampel}}")
        st.info("A: Blanko, B: Sampel, N: Normalitas FAS, V: Vol Sampel Air")

    st.markdown("---")
    
    # Input Identitas & Data
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("👤 Identitas Pengambilan")
        nama_petugas = st.text_input("Nama Petugas Pengambil Contoh", placeholder="Contoh: Budi Santoso")
        nama_sampel = st.text_input("Kode/Lokasi Sampel", placeholder="Contoh: Outlet IPAL 01")
        
    with col_input2:
        st.subheader("📋 Ambang Batas")
        baku_opsi = {"Domestik (100 mg/L)": 100, "Tekstil (150 mg/L)": 150, "Cat (100 mg/L)": 100, "Custom": 0}
        pilihan = st.selectbox("Pilih Baku Mutu:", list(baku_opsi.keys()))
        limit = st.number_input("Batas Maksimal (mg/L)", value=baku_opsi[pilihan]) if pilihan == "Custom" else baku_opsi[pilihan]

    st.markdown("### 📥 Data Hasil Titrasi")
    c1, c2, c3, c4 = st.columns(4)
    v_blanko = c1.number_input("Vol Blanko (A)", value=10.0)
    v_sampel = c2.number_input("Vol Sampel (B)", value=6.5)
    norm = c3.number_input("Normalitas (N)", value=0.1000, format="%.4f")
    v_air = c4.number_input("Vol Air (mL)", value=25.0)

    if st.button("🚀 HITUNG & SIMPAN HASIL"):
        if nama_petugas == "" or nama_sampel == "":
            st.error("⚠️ Nama Petugas dan Lokasi Sampel harus diisi!")
        else:
            # Perhitungan
            hasil = ((v_blanko - v_sampel) * norm * 8000) / v_air
            waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Interpretasi
            if hasil <= limit:
                status = "LOLOS ✅"
                interpretasi = f"Kadar COD {hasil:.2f} mg/L memenuhi syarat baku mutu ({limit} mg/L). Air limbah aman dialirkan."
            else:
                status = "TIDAK LOLOS ❌"
                interpretasi = f"Kadar COD {hasil:.2f} mg/L melebihi ambang batas ({limit} mg/L). Diperlukan pengolahan ulang pada IPAL."

            # Tampilkan Hasil
            st.markdown(f"""
            <div class="custom-card" style="border-left: 5px solid {'#10b981' if hasil <= limit else '#ef4444'}">
                <h4>Hasil Analisis - {nama_sampel}</h4>
                <p><b>Petugas:</b> {nama_petugas} | <b>Waktu:</b> {waktu_skrg}</p>
                <h2 style="text-align: left !important;">{hasil:.2f} mg/L</h2>
                <p><b>Status:</b> {status}</p>
                <p><b>Interpretasi:</b> {interpretasi}</p>
            </div>
            """, unsafe_allow_html=True)

            # Simpan ke Riwayat (CSV)
            new_data = pd.DataFrame([[waktu_skrg, nama_petugas, nama_sampel, limit, round(hasil,2), status, interpretasi]], 
                                    columns=["Waktu", "Petugas", "Sampel", "Baku Mutu", "Hasil (mg/L)", "Status", "Interpretasi"])
            new_data.to_csv(NAMA_FILE_HISTORY, mode='a', header=False, index=False)
            st.toast("Data berhasil disimpan ke riwayat!")

# --- HALAMAN RIWAYAT ---
elif menu == "📜 Riwayat & Laporan":
    st.markdown("<h1>Riwayat Pengujian COD</h1>", unsafe_allow_html=True)
    
    df_history = pd.read_csv(NAMA_FILE_HISTORY)
    
    if df_history.empty:
        st.warning("Belum ada riwayat perhitungan.")
    else:
        # Tampilkan Tabel
        st.dataframe(df_history, use_container_width=True)
        
        # Fitur Unduh
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Laporan (CSV)",
            data=csv,
            file_name=f"Laporan_COD_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
        
        if st.button("🗑️ Bersihkan Semua Riwayat"):
            df_empty = pd.DataFrame(columns=["Waktu", "Petugas", "Sampel", "Baku Mutu", "Hasil (mg/L)", "Status", "Interpretasi"])
            df_empty.to_csv(NAMA_FILE_HISTORY, index=False)
            st.rerun()

# --- HALAMAN TENTANG ---
elif menu == "ℹ️ Tentang":
    st.markdown("<h1>Tentang Aplikasi</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-card">
        <h3>Referensi Regulasi</h3>
        <ul>
            <li><b>SNI 6989.2:2019:</b> Metode pengujian COD dengan titrasi.</li>
            <li><b>Permen LHK No. 68/2016:</b> Baku mutu air limbah domestik.</li>
            <li><b>PP No. 22 Tahun 2021:</b> Pengelolaan kualitas air dan pengendalian pencemaran.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
