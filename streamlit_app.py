import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="EcoEng Simulator IPAL Pro", layout="wide")

# --- JUDUL APLIKASI ---
st.title("🌊 Digital Twin: Simulator Pengolahan Limbah Pro")
st.markdown("Alat simulasi presisi untuk perancangan dimensi unit IPAL dan prediksi kualitas outlet.")

# --- SIDEBAR: INPUT PARAMETER ---
st.sidebar.header("🛠️ Parameter Input Limbah")
debit = st.sidebar.number_input("Debit Air Limbah (m³/hari)", min_value=1.0, value=500.0, step=10.0)
bod_in = st.sidebar.number_input("BOD Inlet (mg/L)", min_value=1.0, value=300.0)

st.sidebar.divider()
st.sidebar.header("⚙️ Konfigurasi Desain")
hrt_target = st.sidebar.slider("Waktu Tinggal / HRT (Jam)", 1, 48, 24)

# --- LOGIKA PERHITUNGAN TEKNIK ---
# Estimasi Efisiensi (Sederhana: Kinetika Orde 1)
k = 0.15 # Konstanta degradasi (bisa disesuaikan)
bod_out = bod_in * np.exp(-k * hrt_target)
efisiensi = ((bod_in - bod_out) / bod_in) * 100

# --- MAIN CONTENT ---
# Menggunakan kolum untuk tata letak yang lebih rapi
col1, col2 = st.columns([1, 2])

# Kolom 1: Menampilkan metrik utama
with col1:
    st.subheader("Ringkasan Performa")
    st.metric("Prediksi BOD Outlet", f"{bod_out:.1f} mg/L", delta_color="inverse")
    st.metric("Efisiensi Sistem", f"{efisiensi:.1f}%")

    # Cek Regulasi (Contoh standar Baku Mutu: 30 mg/L)
    baku_mutu_bod = 30.0
    if bod_out <= baku_mutu_bod:
        st.success(f"✅ AMAN: Memenuhi syarat (di bawah {baku_mutu_bod} mg/L).")
    else:
        st.error(f"⚠️ BAHAYA: MELEBIHI ambang batas ({baku_mutu_bod} mg/L).")

# Kolom 2: Menampilkan visualisasi gauge
with col2:
    st.subheader("Visualisasi Kualitas Akhir")
    
    # Membuat visualisasi gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bod_out,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Kadar BOD Akhir (mg/L)"},
        gauge = {
            'axis': {'range': [0, bod_in]}, # Rentang dari 0 hingga BOD Inlet
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"}, # Zona Aman
                {'range': [30, bod_in], 'color': "pink"}    # Zona Bahaya
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30 # Ambang batas baku mutu
            }
        }
    ))

    # Menampilkan gauge di Streamlit
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("EcoEng Simulator Pro v1.1 | Dikembangkan dengan Streamlit dan Plotly")
