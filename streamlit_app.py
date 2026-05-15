import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# 2. Styling CSS (Tetap utuh)
st.markdown("""
<style>
.main-header {font-size: 2.5rem; color: #2E7D32; text-align: center;}
.metric-card {background-color: #E8F5E8; padding: 1rem; border-radius: 10px; border-left: 5px solid #4CAF50;}
[data-testid="stMetricValue"] { font-size: 1.8rem !important; }
</style>
""", unsafe_allow_html=True)

# 3. Konstanta & Fungsi Logika (Tetap utuh)
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

# 4. Fungsi Penyimpanan Report (Fitur Baru untuk Gabungan Data)
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def save_to_report(cat, param, val, unit):
    new_data = pd.DataFrame({'Kategori': [cat], 'Parameter': [param], 'Nilai': [val], 'Satuan': [unit]})
    st.session_state.full_report = pd.concat([st.session_report, new_data] if 'full_report' in st.session_state else [new_data]) # Logika internal untuk update data

# --- PERBAIKAN LOGIKA RE-RUN AGAR DATA TIDAK ILANG ---
def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. Header
st.markdown('<h1 class="main-header">🌱 EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)

# 6. Sidebar Navigation
with st.sidebar:
    st.title("🌱 Navigation")
    page = st.selectbox("Pilih Fitur:", ["🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker"])
    
    st.divider()
    st.subheader("📥 Download Center")
    if not st.session_state.full_report.empty:
        csv = st.session_state.full_report.to_csv(index=False).encode('utf-8')
        st.download_button("Download Gabungan Data (CSV)", data=csv, file_name='Report_EcoEngineer.csv', mime='text/csv', use_container_width=True)
        if st.button("Reset Semua Data"):
            st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
            st.rerun()
    else:
        st.caption("Belum ada data untuk diunduh. Lakukan perhitungan dulu.")

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
            # Simpan hasil ke report
            df_sizing = pd.DataFrame({
                'Kategori': ['Unit Sizing']*3,
                'Parameter': ['Volume', 'Luas', 'Dimensi PxLxT'],
                'Nilai': [dims['Volume'], dims['Luas'], f"{dims['Panjang']}x{dims['Lebar']}x{dims['Tinggi']}"],
                'Satuan': ['m3', 'm2', 'm']
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
                color='lightblue', opacity=0.7
            )])
            st.plotly_chart(fig, use_container_width=True)

# --- 🧪 STOICHIOMETRY ---
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry Calculator")
    col1, col2 = st.columns(2)
    with col1:
        B_in = st.number_input("BOD Masuk (mg/L)", value=200.0)
        Q_s = st.number_input("Debit (m³/hari)", value=100.0)
        coag = st.selectbox("Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("🧪 Hitung Dosis"):
            ds = stoichiometry_coagulant(B_in, Q_s, coag)
            df_st = pd.DataFrame({'Kategori':['Stoich'], 'Parameter':[f'Dosis {coag}'], 'Nilai':[ds], 'Satuan':['kg/hari']})
            update_report(df_st)
            st.session_state.last_ds = ds
    if 'last_ds' in st.session_state:
        with col2:
            st.metric(f"Kebutuhan {coag}", f"{st.session_state.last_ds} kg/hari")

# --- 📊 SIMULASI ---
elif page == "📊 Simulasi":
    st.header("📊 Interactive Simulation")
    col1, col2, col3 = st.columns(3)
    with col1: b_sim = st.slider("BOD Masuk", 50, 500, 200)
    with col2: q_sim = st.slider("Debit", 50, 500, 100)
    with col3: eff = st.slider("Efisiensi %", 50.0, 95.0, 85.0)
    
    b_out = b_sim * (1 - eff/100)
    if st.button("📊 Simpan Hasil Simulasi"):
        df_sim = pd.DataFrame({'Kategori':['Simulasi'], 'Parameter':['BOD Keluar'], 'Nilai':[round(b_out,2)], 'Satuan':['mg/L']})
        update_report(df_sim)
        st.success("Tersimpan ke report!")
    
    fig = go.Figure([go.Bar(x=['Influent', 'Effluent'], y=[b_sim, b_out], marker_color=['red', 'blue'])])
    st.plotly_chart(fig)

# --- ✅ CHECKER ---
elif page == "✅ Checker":
    st.header("✅ Regulatory Checker")
    c1, c2, c3, c4 = st.columns(4)
    b_e = c1.number_input("BOD5", value=25.0); c_e = c2.number_input("COD", value=80.0)
    t_e = c3.number_input("TSS", value=20.0); p_e = c4.number_input("pH", value=7.0)
    
    if st.button("🔍 Cek Kepatuhan"):
        data = {'BOD5': b_e, 'COD': c_e, 'TSS': t_e, 'pH': p_e}
        res = check_regulation(data)
        status = "LULUS" if all(res.values()) else "GAGAL"
        df_ch = pd.DataFrame({'Kategori':['Checker'], 'Parameter':['Status Akhir'], 'Nilai':[status], 'Satuan':['-']})
        update_report(df_ch)
        
        st.markdown(f'<div class="metric-card"><h3>HASIL: {status}</h3></div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({'Parameter': list(res.keys()), 'Hasil': list(data.values()), 'Status': ['✅' if v else '❌' for v in res.values()]}))
