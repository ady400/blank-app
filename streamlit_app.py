import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# 2. Styling CSS
st.markdown("""
<style>
.main-header {font-size: 2.5rem; color: #2E7D32; text-align: center;}
.metric-card {background-color: #E8F5E8; padding: 1rem; border-radius: 10px; border-left: 5px solid #4CAF50;}
[data-testid="stMetricValue"] { font-size: 1.8rem !important; }
</style>
""", unsafe_allow_html=True)

# 3. Konstanta & Fungsi Logika
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9)}

def calculate_unit_sizing(Q, td, surface_loading_rate=24):
    V = Q * td / 24
    A = Q / surface_loading_rate
    H = 3.5
    L = math.sqrt(A * 3)
    W = math.sqrt(A / 3)
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

def stoichiometry_coagulant(BOD_in, Q, coagulant_type='FeCl3'):
    ratios = {'FeCl3': 8, 'Alum': 10, 'PAC': 6}
    dosage = BOD_in * ratios.get(coagulant_type, 8) * Q / 1000
    return round(dosage, 2)

def check_regulation(effluent):
    status = {}
    for param, limit in BAKU_MUTU.items():
        if param == 'pH':
            status[param] = effluent[param] >= limit[0] and effluent[param] <= limit[1]
        else:
            status[param] = effluent[param] <= limit
    return status

# 4. Fungsi Management Report
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True)
    # Hapus duplikat agar parameter yang sama terupdate ke nilai terbaru
    st.session_state.full_report = st.session_state.full_report.drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. Header Utama
st.markdown('<h1 class="main-header">🌱 EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)

# 6. Sidebar Navigation & Download
with st.sidebar:
    st.title("🌱 Navigation")
    page = st.selectbox("Pilih Fitur:", ["🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker"])
    
    st.divider()
    st.subheader("📥 Download Center")
    
    if not st.session_state.full_report.empty:
        # Menyiapkan DataFrame yang rapi untuk didownload
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Membuat DataFrame Header untuk estetika file
        header_df = pd.DataFrame([
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Waktu Generate: {current_time}", "", "", ""],
            ["-"*50, "-"*20, "-"*20, "-"*10],
            ["KATEGORI", "PARAMETER", "NILAI", "SATUAN"]
        ], columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        
        # Gabungkan Header dengan Data Utama
        final_download_df = pd.concat([header_df, st.session_state.full_report], ignore_index=True)
        
        csv = final_download_df.to_csv(index=False, header=False).encode('utf-8')
        
        st.success("Data siap diunduh!")
        st.download_button(
            label="Download Full Report (CSV)",
            data=csv,
            file_name=f'Report_EcoEngineer_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        if st.button("🗑️ Reset Data Report"):
            st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
            st.rerun()
    else:
        st.info("Belum ada data. Silakan lakukan perhitungan di menu fitur.")

# 7. Konten Halaman

# --- 🏗️ UNIT SIZING ---
if page == "🏗️ Unit Sizing":
    st.header("🏗️ Automatic Unit Sizing")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Input Data")
        Q = st.number_input("**Debit (Q)** (m³/hari)", min_value=1.0, value=100.0)
        td = st.number_input("**Waktu Tinggal (t_d)** (jam)", min_value=1.0, value=24.0)
        SLR = st.number_input("**Surface Loading Rate**", min_value=5.0, value=24.0)
        
        if st.button("💾 Hitung Dimensi", type="primary", use_container_width=True):
            dims = calculate_unit_sizing(Q, td, SLR)
            # Simpan ke Report
            df_sizing = pd.DataFrame({
                'Kategori': ['Unit Sizing']*4,
                'Parameter': ['Volume Bak', 'Luas Permukaan', 'Dimensi (PxLxT)', 'Tinggi Jagaan'],
                'Nilai': [dims['Volume'], dims['Luas'], f"{dims['Panjang']} x {dims['Lebar']} x {dims['Tinggi']}", 3.5],
                'Satuan': ['m3', 'm2', 'meter', 'meter']
            })
            update_report(df_sizing)
            st.session_state.last_dims = dims

    if 'last_dims' in st.session_state:
        with col2:
            d = st.session_state.last_dims
            st.subheader("📐 Hasil Dimensi Bak")
            m1, m2, m3 = st.columns(3)
            m1.metric("Volume", f"{d['Volume']} m³")
            m2.metric("Luas", f"{d['Luas']} m²")
            m3.markdown(f"**P x L x T (m):**\n### {d['Panjang']} x {d['Lebar']} x {d['Tinggi']}")
            
            fig = go.Figure(data=[go.Mesh3d(
                x=[0, d['Panjang'], d['Panjang'], 0, 0, d['Panjang'], d['Panjang'], 0],
                y=[0, 0, d['Lebar'], d['Lebar'], 0, 0, d['Lebar'], d['Lebar']],
                z=[0, 0, 0, 0, d['Tinggi'], d['Tinggi'], d['Tinggi'], d['Tinggi']],
                color='lightgreen', opacity=0.8
            )])
            fig.update_layout(scene=dict(xaxis_title='P', yaxis_title='L', zaxis_title='T'), margin=dict(l=0,r=0,b=0,t=0))
            st.plotly_chart(fig, use_container_width=True)

# --- 🧪 STOICHIOMETRY ---
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry Calculator")
    col1, col2 = st.columns(2)
    with col1:
        B_in = st.number_input("BOD Masuk (mg/L)", value=200.0)
        Q_s = st.number_input("Debit Air Limbah (m³/hari)", value=100.0)
        coag = st.selectbox("Pilih Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("🧪 Hitung Dosis Koagulan"):
            ds = stoichiometry_coagulant(B_in, Q_s, coag)
            df_st = pd.DataFrame({
                'Kategori': ['Stoichiometry'],
                'Parameter': [f'Kebutuhan {coag}'],
                'Nilai': [ds],
                'Satuan': ['kg/hari']
            })
            update_report(df_st)
            st.session_state.last_ds = ds
    if 'last_ds' in st.session_state:
        with col2:
            st.info(f"Berdasarkan rasio stoikiometri, kebutuhan koagulan **{coag}** Anda adalah:")
            st.metric(f"{coag}", f"{st.session_state.last_ds} kg/hari")

# --- 📊 SIMULASI ---
elif page == "📊 Simulasi":
    st.header("📊 Interactive Performance Simulation")
    col1, col2, col3 = st.columns(3)
    b_sim = col1.slider("BOD In (mg/L)", 50, 500, 200)
    eff = col2.slider("Efisiensi (%)", 50.0, 95.0, 85.0)
    b_out = b_sim * (1 - eff/100)
    
    col3.metric("Estimasi BOD Out", f"{round(b_out, 2)} mg/L")
    
    if st.button("📊 Simpan Hasil Simulasi ke Report"):
        df_sim = pd.DataFrame({
            'Kategori': ['Simulasi'],
            'Parameter': ['Estimasi BOD Effluent'],
            'Nilai': [round(b_out, 2)],
            'Satuan': ['mg/L']
        })
        update_report(df_sim)
        st.success("Hasil simulasi berhasil ditambahkan ke laporan!")
    
    st.bar_chart({'Influent (BOD)': b_sim, 'Effluent (BOD)': b_out})

# --- ✅ CHECKER ---
elif page == "✅ Checker":
    st.header("✅ Regulatory Compliance Checker")
    st.write("Bandingkan hasil analisa laboratorium dengan Baku Mutu (Permen LHK No. P.68/2016)")
    
    c1, c2, c3, c4 = st.columns(4)
    b_e = c1.number_input("BOD5 (mg/L)", value=25.0)
    c_e = c2.number_input("COD (mg/L)", value=80.0)
    t_e = c3.number_input("TSS (mg/L)", value=20.0)
    p_e = c4.number_input("pH", value=7.0, min_value=0.0, max_value=14.0)
    
    if st.button("🔍 Jalankan Pemeriksaan"):
        data = {'BOD5': b_e, 'COD': c_e, 'TSS': t_e, 'pH': p_e}
        res = check_regulation(data)
        status = "LULUS" if all(res.values()) else "GAGAL"
        
        df_ch = pd.DataFrame({
            'Kategori': ['Regulatory Checker'],
            'Parameter': ['Status Kepatuhan Akhir'],
            'Nilai': [status],
            'Satuan': ['Status']
        })
        update_report(df_ch)
        
        color = "#4CAF50" if status == "LULUS" else "#F44336"
        st.markdown(f'<div class="metric-card" style="border-left-color: {color}"><h3 style="color: {color}">{status} Baku Mutu</h3></div>', unsafe_allow_html=True)
        
        st.table(pd.DataFrame({
            'Parameter': list(res.keys()),
            'Hasil Analisa': list(data.values()),
            'Baku Mutu Max': [30, 100, 30, "6.0 - 9.0"],
            'Keterangan': ['✅ Aman' if v else '❌ Melebihi Ambang' for v in res.values()]
        }))
