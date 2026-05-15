import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# Fungsi untuk memuat animasi Lottie
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Link Animasi Lottie untuk Setiap Halaman
lottie_links = {
    "Intro": "https://assets10.lottiefiles.com/packages/lf20_m9ubtsbe.json", # Alam/Eco
    "Sizing": "https://assets3.lottiefiles.com/packages/lf20_iv4ce798.json", # Konstruksi/Pabrik
    "Stoich": "https://assets5.lottiefiles.com/packages/lf20_v7rzhxbi.json", # Kimia/Lab
    "Sim": "https://assets1.lottiefiles.com/packages/lf20_qp1q7mct.json",    # Grafik/Data
    "Check": "https://assets9.lottiefiles.com/packages/lf20_i9m86sco.json"   # Centang/Verifikasi
}

# 2. Styling CSS
st.markdown("""
<style>
.main-header {font-size: 3rem; color: #2E7D32; font-weight: bold;}
.intro-text {font-size: 1.2rem; color: #424242; line-height: 1.6;}
.metric-card {background-color: #E8F5E8; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #4CAF50;}
.footer {text-align: center; margin-top: 50px; color: #757575; border-top: 1px solid #e0e0e0; padding-top: 20px;}
</style>
""", unsafe_allow_html=True)

# 3. Logika Backend (Sizing, Stoich, Check)
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

# 4. Global State & Report Management
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True)
    st.session_state.full_report = st.session_state.full_report.drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. Sidebar
with st.sidebar:
    st.title("🌱 Main Menu")
    page = st.selectbox("Navigasi Halaman:", ["🏠 Intro / Perkenalan", "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker"])
    
    st.divider()
    st.subheader("📥 Download Center")
    if not st.session_state.full_report.empty:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_text = [
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Waktu Generate: {current_time}", "", "", ""],
            ["Pembuat: [Nama Anda/Tim Anda]", "", "", ""],
            ["-"*40, "-"*20, "-"*20, "-"*10],
            ["KATEGORI", "PARAMETER", "NILAI", "SATUAN"]
        ]
        header_df = pd.DataFrame(header_text, columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        final_df = pd.concat([header_df, st.session_state.full_report], ignore_index=True)
        csv = final_df.to_csv(index=False, header=False).encode('utf-8')
        st.download_button("Download Report (CSV)", data=csv, file_name=f'Report_{datetime.now().strftime("%Y%m%d")}.csv', mime='text/csv', use_container_width=True)
    
    st.divider()
    st.caption("**Referensi:**\n- Permen LHK P.68/2016\n- Metcalf & Eddy (Wastewater Engineering)")

# 6. Konten Halaman

# --- 🏠 HALAMAN INTRO ---
if page == "🏠 Intro / Perkenalan":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<h1 class="main-header">Selamat Datang di <br>EcoEngineer Pro-Dash!</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div class="intro-text">
        EcoEngineer Pro-Dash adalah platform digital mutakhir untuk membantu <b>Insinyur Lingkungan</b> 
        dalam merancang dan memantau unit pengolahan air limbah secara presisi.
        <br><br>
        <b>Fitur Utama Kami:</b>
        <ul>
            <li><b>🏗️ Unit Sizing:</b> Perhitungan dimensi bak secara otomatis (PxLxT).</li>
            <li><b>🧪 Stoichiometry:</b> Estimasi kebutuhan koagulan (FeCl3, Alum, PAC).</li>
            <li><b>📊 Simulasi:</b> Prediksi kualitas effluent berdasarkan efisiensi alat.</li>
            <li><b>✅ Checker:</b> Verifikasi kepatuhan terhadap regulasi Permen LHK No. 68 Tahun 2016.</li>
        </ul>
        <p><i>Silakan pilih fitur di menu sidebar untuk memulai!</i></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        anim = load_lottieurl(lottie_links["Intro"])
        st_lottie(anim, height=350, key="intro_anim")

# --- 🏗️ UNIT SIZING ---
elif page == "🏗️ Unit Sizing":
    col_t, col_a = st.columns([3, 1])
    with col_t: st.header("🏗️ Automatic Unit Sizing")
    with col_a: st_lottie(load_lottieurl(lottie_links["Sizing"]), height=100, key="sizing_anim")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        Q = st.number_input("Debit (Q) (m³/hari)", value=100.0)
        td = st.number_input("Waktu Tinggal (jam)", value=24.0)
        SLR = st.number_input("SLR (m³/m².hari)", value=24.0)
        if st.button("💾 Hitung & Simpan", type="primary", use_container_width=True):
            dims = calculate_unit_sizing(Q, td, SLR)
            update_report(pd.DataFrame({'Kategori':['Unit Sizing']*3, 'Parameter':['Volume', 'Luas', 'Dimensi'], 'Nilai':[dims['Volume'], dims['Luas'], f"{dims['Panjang']}x{dims['Lebar']}x{dims['Tinggi']}"], 'Satuan':['m3', 'm2', 'meter']}))
            st.session_state.last_dims = dims

    if 'last_dims' in st.session_state:
        with col2:
            d = st.session_state.last_dims
            m1, m2, m3 = st.columns(3)
            m1.metric("Volume", f"{d['Volume']} m³")
            m2.metric("Luas", f"{d['Luas']} m²")
            m3.markdown(f"**Dimensi PxLxT:**\n### {d['Panjang']}x{d['Lebar']}x{d['Tinggi']} m")
            fig = go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,d['Tinggi'],d['Tinggi'],d['Tinggi'],d['Tinggi']], color='lightgreen', opacity=0.8)])
            st.plotly_chart(fig, use_container_width=True)

# --- 🧪 STOICHIOMETRY ---
elif page == "🧪 Stoichiometry":
    col_t, col_a = st.columns([3, 1])
    with col_t: st.header("🧪 Stoichiometry Calculator")
    with col_a: st_lottie(load_lottieurl(lottie_links["Stoich"]), height=100, key="stoich_anim")
    
    col1, col2 = st.columns(2)
    with col1:
        B_in = st.number_input("BOD Masuk (mg/L)", value=200.0)
        Q_s = st.number_input("Debit (m³/hari)", value=100.0)
        coag = st.selectbox("Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("🧪 Hitung Dosis"):
            ds = stoichiometry_coagulant(B_in, Q_s, coag)
            update_report(pd.DataFrame({'Kategori':['Stoich'], 'Parameter':[f'Dosis {coag}'], 'Nilai':[ds], 'Satuan':['kg/hari']}))
            st.session_state.last_ds = ds
    if 'last_ds' in st.session_state:
        col2.metric(f"Dosis {coag}", f"{st.session_state.last_ds} kg/hari")

# --- 📊 SIMULASI ---
elif page == "📊 Simulasi":
    col_t, col_a = st.columns([3, 1])
    with col_t: st.header("📊 Performance Simulation")
    with col_a: st_lottie(load_lottieurl(lottie_links["Sim"]), height=100, key="sim_anim")
    
    b_in = st.slider("BOD Influent", 50, 500, 200)
    eff = st.slider("Efisiensi (%)", 50.0, 95.0, 85.0)
    b_out = round(b_in * (1 - eff/100), 2)
    st.metric("Estimasi Effluent", f"{b_out} mg/L")
    st.bar_chart({'Influent': b_in, 'Effluent': b_out})

# --- ✅ CHECKER ---
elif page == "✅ Checker":
    col_t, col_a = st.columns([3, 1])
    with col_t: st.header("✅ Regulatory Compliance Checker")
    with col_a: st_lottie(load_lottieurl(lottie_links["Check"]), height=100, key="check_anim")
    
    c1, c2, c3, c4 = st.columns(4)
    data = {'BOD5': c1.number_input("BOD5", 25.0), 'COD': c2.number_input("COD", 80.0), 'TSS': c3.number_input("TSS", 20.0), 'pH': c4.number_input("pH", 7.0)}
    if st.button("🔍 Jalankan Pemeriksaan"):
        res = check_regulation(data)
        status = "LULUS" if all(res.values()) else "GAGAL"
        st.markdown(f'<div class="metric-card"><h3>HASIL: {status}</h3></div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({'Parameter': list(res.keys()), 'Hasil': list(data.values()), 'Status': ['✅' if v else '❌' for v in res.values()]}))

# 8. Footer
st.markdown(f"""
<div class="footer">
    <p><b>EcoEngineer Pro-Dash v1.0</b> | © {datetime.now().year}</p>
    <p>Dikembangkan oleh: <b>[Nama Anda/Tim Anda]</b></p>
</div>
""", unsafe_allow_html=True)
