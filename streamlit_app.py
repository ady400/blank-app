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

# Fungsi Load Lottie yang Lebih Aman
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Link Animasi Alternatif (Jika link utama mati, aplikasi tidak akan error)
# Saya gunakan link yang biasanya sangat stabil
lottie_links = {
    "Intro": "https://lottie.host/80516b34-897b-4029-8797-29007c570993/9nL0o0iYkS.json", # Nature/Eco
    "Sizing": "https://lottie.host/9e4871e9-4e08-466d-96f7-3c976f62664d/U0V166S04A.json", # Construction
    "Stoich": "https://lottie.host/318041c2-1925-4674-8d48-693175f0f353/Y9V4vXzT1j.json", # Science/Lab
    "Sim": "https://lottie.host/22b9f3d9-9520-4100-8802-5e3789431e56/m4a9xK8I0i.json",    # Data
    "Check": "https://lottie.host/97f7429b-7561-4560-843c-6623e6179b9d/I8pB1X8E0A.json"   # Verifikasi
}

# 2. Styling CSS
st.markdown("""
<style>
.main-header {font-size: 3rem; color: #2E7D32; font-weight: bold;}
.metric-card {background-color: #E8F5E8; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #4CAF50;}
.footer {text-align: center; margin-top: 50px; color: #757575; border-top: 1px solid #e0e0e0; padding-top: 20px;}
</style>
""", unsafe_allow_html=True)

# 3. Logika Utama
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9)}

def calculate_unit_sizing(Q, td, SLR=24):
    V, A, H = (Q * td / 24), (Q / SLR), 3.5
    L, W = math.sqrt(A * 3), math.sqrt(A / 3)
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

def stoichiometry_coagulant(BOD_in, Q, coagulant_type='FeCl3'):
    ratios = {'FeCl3': 8, 'Alum': 10, 'PAC': 6}
    return round(BOD_in * ratios.get(coagulant_type, 8) * Q / 1000, 2)

def check_regulation(eff):
    return {p: (eff[p] >= BAKU_MUTU[p][0] and eff[p] <= BAKU_MUTU[p][1]) if p == 'pH' else eff[p] <= BAKU_MUTU[p] for p in BAKU_MUTU}

# 4. Report Management
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. Sidebar
with st.sidebar:
    st.title("🌱 Menu Utama")
    page = st.selectbox("Navigasi:", ["🏠 Beranda Intro", "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker"])
    
    st.divider()
    if not st.session_state.full_report.empty:
        header_text = [
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Waktu Generate: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "", "", ""],
            ["Pembuat: [Nama Anda/Tim Anda]", "", "", ""],
            ["="*40, "="*20, "="*20, "="*10]
        ]
        header_df = pd.DataFrame(header_text, columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        final_df = pd.concat([header_df, st.session_state.full_report], ignore_index=True)
        st.download_button("📥 Download Report (CSV)", data=final_df.to_csv(index=False, header=False).encode('utf-8'), file_name='Report_EcoEngineer.csv', mime='text/csv', use_container_width=True)

# 6. Jalankan Halaman
anim_data = load_lottieurl(lottie_links.get("Intro" if page.startswith("🏠") else "Sizing" if "Unit" in page else "Stoich" if "Stoic" in page else "Sim" if "Sim" in page else "Check"))

if page == "🏠 Beranda Intro":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<h1 class="main-header">EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)
        st.write("### Solusi Digital Pengolahan Air Limbah")
        st.write("Aplikasi ini dirancang untuk memudahkan Insinyur Lingkungan dalam menghitung dimensi unit, dosis kimia, hingga pengecekan baku mutu dalam satu platform.")
    with c2: st_lottie(anim_data, height=250) if anim_data else st.image("https://via.placeholder.com/250?text=Eco+Engineer")

elif page == "🏗️ Unit Sizing":
    st.header("🏗️ Unit Sizing")
    col_in, col_res = st.columns([1, 2])
    with col_in:
        Q = st.number_input("Debit (m³/hari)", value=100.0); td = st.number_input("Waktu Tinggal (jam)", value=24.0)
        if st.button("Hitung Dimensi"):
            d = calculate_unit_sizing(Q, td)
            st.session_state.last_dims = d
            update_report(pd.DataFrame({'Kategori':['Unit Sizing']*3, 'Parameter':['Volume','Luas','Dimensi'], 'Nilai':[d['Volume'],d['Luas'],f"{d['Panjang']}x{d['Lebar']}x{d['Tinggi']}"], 'Satuan':['m3','m2','m']}))
    
    if 'last_dims' in st.session_state:
        with col_res:
            d = st.session_state.last_dims
            st.metric("Volume Bak", f"{d['Volume']} m³")
            st.write(f"**Dimensi:** {d['Panjang']}m x {d['Lebar']}m x {d['Tinggi']}m")
            st.plotly_chart(go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,d['Tinggi'],d['Tinggi'],d['Tinggi'],d['Tinggi']], color='lightgreen', opacity=0.8)]), use_container_width=True)

elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry")
    b_in = st.number_input("BOD Masuk (mg/L)", value=200.0); q_s = st.number_input("Debit (m³/hari)", value=100.0)
    coag = st.selectbox("Koagulan", ['FeCl3', 'Alum', 'PAC'])
    if st.button("Hitung Dosis"):
        res = stoichiometry_coagulant(b_in, q_s, coag)
        st.metric(f"Dosis {coag}", f"{res} kg/hari")
        update_report(pd.DataFrame({'Kategori':['Stoich'], 'Parameter':[f'Dosis {coag}'], 'Nilai':[res], 'Satuan':['kg/hari']}))

elif page == "📊 Simulasi":
    st.header("📊 Simulasi")
    eff = st.slider("Efisiensi (%)", 50.0, 99.0, 85.0)
    b_in_s = st.number_input("BOD In", value=200.0)
    b_out = round(b_in_s * (1 - eff/100), 2)
    st.metric("Estimasi BOD Keluar", f"{b_out} mg/L")
    st.bar_chart({'Influent': b_in_s, 'Effluent': b_out})
    if st.button("Simpan Simulasi"):
        update_report(pd.DataFrame({'Kategori':['Simulasi'], 'Parameter':['BOD Out'], 'Nilai':[b_out], 'Satuan':['mg/L']}))

elif page == "✅ Checker":
    st.header("✅ Baku Mutu Checker")
    val = {'BOD5': st.number_input("BOD5", 25.0), 'COD': st.number_input("COD", 80.0), 'TSS': st.number_input("TSS", 20.0), 'pH': st.number_input("pH", 7.0)}
    if st.button("Cek Regulasi"):
        res = check_regulation(val)
        status = "LULUS" if all(res.values()) else "GAGAL"
        st.subheader(f"Status: {status}")
        st.table(pd.DataFrame({'Parameter': res.keys(), 'Hasil': val.values(), 'Status': ['✅' if v else '❌' for v in res.values()]}))
        update_report(pd.DataFrame({'Kategori':['Checker'], 'Parameter':['Status Akhir'], 'Nilai':[status], 'Satuan':['-']}))

# 7. Footer
st.markdown(f'<div class="footer"><p><b>EcoEngineer Pro-Dash</b> | © {datetime.now().year}<br>Referensi: Permen LHK P.68/2016</p></div>', unsafe_allow_html=True)
