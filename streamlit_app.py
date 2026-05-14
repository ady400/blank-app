import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="EcoEng Simulator IPAL", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT PARAMETER ---
st.sidebar.header("🛠️ Parameter Input Limbah")
debit = st.sidebar.number_input("Debit Air Limbah (m³/hari)", min_value=1.0, value=500.0, step=10.0)
bod_in = st.sidebar.number_input("BOD Inlet (mg/L)", min_value=1.0, value=300.0)
tss_in = st.sidebar.number_input("TSS Inlet (mg/L)", min_value=1.0, value=250.0)

st.sidebar.divider()
st.sidebar.header("⚙️ Konfigurasi Desain")
hrt_target = st.sidebar.slider("Waktu Tinggal / HRT (Jam)", 1, 48, 24)
kedalaman_rencana = st.sidebar.slider("Rencana Kedalaman Bak (m)", 1.5, 5.0, 3.0)

# --- LOGIKA PERHITUNGAN TEKNIK ---
# 1. Perhitungan Volume Bak
volume_m3 = (debit / 24) * hrt_target
luas_permukaan = volume_m3 / kedalaman_rencana

# 2. Estimasi Efisiensi (Sederhana: Kinetika Orde 1)
# Misal konstanta degradasi k = 0.15 / jam
k = 0.15
bod_out = bod_in * np.exp(-k * hrt_target)
efisiensi = ((bod_in - bod_out) / bod_in) * 100

# --- MAIN CONTENT ---
st.title("🌊 Digital Twin: Simulator Pengolahan Limbah")
st.markdown("Alat simulasi presisi untuk perancangan dimensi unit IPAL dan prediksi kualitas outlet.")

# Kolom Ringkasan
col1, col2, col3, col4 = st.columns(4)
col1.metric("Volume Reaktor", f"{volume_m3:.1f} m³")
col2.metric("Luas Lahan", f"{luas_permukaan:.1f} m²")
col3.metric("Prediksi BOD Outlet", f"{bod_out:.1f} mg/L")
col4.metric("Efisiensi Sistem", f"{efisiensi:.1f}%")

st.divider()

# Tab Area
tab1, tab2, tab3 = st.tabs(["📊 Analisis Performa", "📐 Dimensi Teknik", "📜 Cek Regulasi"])

with tab1:
    st.subheader("Simulasi Penurunan Polutan")
    # Membuat data simulasi degradasi sepanjang waktu
    waktu_series = np.linspace(0, hrt_target, 100)
    bod_series = bod_in * np.exp(-k * waktu_series)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=waktu_series, y=bod_series, mode='lines', name='BOD', line=dict(color='green', width=3)))
    fig.update_layout(title="Grafik Penurunan Kadar BOD terhadap Waktu Tinggal",
                     xaxis_title="Waktu (Jam)", yaxis_title="Konsentrasi (mg/L)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Rekomendasi Spesifikasi Unit")
    c1, c2 = st.columns(2)
    
    # Asumsi Bak Persegi Panjang (P = 2L)
    lebar = np.sqrt(luas_permukaan / 2)
    panjang = 2 * lebar
    
    with c1:
        st.write("### Dimensi Fisik")
        df_dimensi = pd.DataFrame({
            "Parameter": ["Panjang", "Lebar", "Kedalaman (SWD)", "Freeboard"],
            "Nilai": [f"{panjang:.2f} m", f"{lebar:.2f} m", f"{kedalaman_rencana:.2f} m", "0.5 m"]
        })
        st.table(df_dimensi)
        
    with c2:
        st.write("### Kebutuhan Oksigen (Air Supply)")
        # Perhitungan kasar kebutuhan udara untuk aerasi
        sor = (debit * (bod_in - bod_out) / 1000) * 1.5 # kg O2/hari
        st.info(f"Estimasi Kebutuhan Oksigen: **{sor:.2f} kg O2/hari**")
        st.write("Gunakan Blower dengan kapasitas minimal 1.2x dari kebutuhan Standar Oxygen Requirement (SOR).")

with tab3:
    st.subheader("Kepatuhan Terhadap Baku Mutu")
    # Contoh standar Baku Mutu (Permen LHK No. 68 Tahun 2016)
    baku_mutu_bod = 30.0
    
    if bod_out <= baku_mutu_bod:
        st.success(f"✅ AMAN: Kadar BOD akhir ({bod_out:.1f}) memenuhi syarat di bawah {baku_mutu_bod} mg/L.")
    else:
        st.error(f"⚠️ BAHAYA: Kadar BOD akhir ({bod_out:.1f}) MELEBIHI ambang batas {baku_mutu_bod} mg/L.")
        st.warning("Saran: Tingkatkan HRT atau tambahkan dosis aerasi.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("EcoEng Simulator v1.0 | Menggunakan Model Kinetika Orde-1")
