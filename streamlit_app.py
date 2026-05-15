import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime
import streamlit.components.v1 as components

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# Fungsi Animasi Lottie via HTML (Solusi Paling Stabil & Anti-Error)
def st_lottie_embed(url, height=200):
    embed_code = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center;">
        <lottie-player src="{url}" background="transparent" speed="1" style="width: {height}px; height: {height}px;" loop autoplay></lottie-player>
    </div>
    """
    return components.html(embed_code, height=height + 10)

# Link Animasi Lottie Terbaru
lottie_links = {
    "Intro": "https://lottie.host/80516b34-897b-4029-8797-29007c570993/9nL0o0iYkS.json",
    "Sizing": "https://lottie.host/9e4871e9-4e08-466d-96f7-3c976f62664d/U0V166S04A.json",
    "Stoich": "https://lottie.host/318041c2-1925-4674-8d48-693175f0f353/Y9V4vXzT1j.json",
    "Sim": "https://lottie.host/22b9f3d9-9520-4100-8802-5e3789431e56/m4a9xK8I0i.json",
    "Check": "https://lottie.host/97f7429b-7561-4560-843c-6623e6179b9d/I8pB1X8E0A.json",
    "About": "https://lottie.host/7e0c4f1c-d72b-4b11-9721-657d90e0e01c/v6W70M7u5I.json"
}

# 2. STYLING CSS CUSTOM
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #2E7D32; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #1B5E20; font-weight: bold; margin-bottom: 10px;}
    .metric-card {background-color: #F1F8E9; padding: 1.5rem; border-radius: 15px; border-left: 8px solid #4CAF50; margin-bottom: 1rem; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);}
    .footer {text-align: center; margin-top: 50px; color: #757575; border-top: 1px solid #eee; padding-top: 20px;}
    .stButton>button {border-radius: 10px; height: 3em; transition: 0.3s;}
    .stButton>button:hover {background-color: #2E7D32; color: white;}
</style>
""", unsafe_allow_html=True)

# 3. LOGIKA BACKEND
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9)}

def calculate_unit_sizing(Q, td, SLR=24):
    V = Q * td / 24
    A = Q / SLR
    H = 3.5
    L = math.sqrt(A * 3)
    W = math.sqrt(A / 3)
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

# 4. REPORT MANAGEMENT (Session State agar data tidak hilang saat navigasi)
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def add_to_report(cat, param, val, unit):
    new_entry = pd.DataFrame({'Kategori': [cat], 'Parameter': [param], 'Nilai': [val], 'Satuan': [unit]})
    st.session_state.full_report = pd.concat([st.session_state.full_report, new_entry], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. SIDEBAR NAVIGATION
with st.sidebar:
    st_lottie_embed(lottie_links["Intro"], height=120)
    st.title("🌱 EcoEngineer Menu")
    page = st.selectbox("Navigasi Fitur:", ["🏠 Beranda / Intro", "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker", "ℹ️ Tentang Web"])
    
    st.divider()
    st.subheader("📥 Export Summary")
    if not st.session_state.full_report.empty:
        # Template Laporan Rapi
        header_data = [
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Tanggal Cetak: {datetime.now().strftime('%d %B %Y %H:%M')}", "", "", ""],
            ["Sumber: Sistem Perhitungan Teknik Lingkungan Terintegrasi", "", "", ""],
            ["-"*50, "-"*20, "-"*20, "-"*10],
            ["KATEGORI", "PARAMETER", "NILAI", "SATUAN"]
        ]
        h_df = pd.DataFrame(header_data, columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        final_csv_df = pd.concat([h_df, st.session_state.full_report], ignore_index=True)
        
        st.download_button(
            label="Download Full Report (CSV)",
            data=final_download_df.to_csv(index=False, header=False).encode('utf-8') if 'final_download_df' in locals() else final_csv_df.to_csv(index=False, header=False).encode('utf-8'),
            file_name=f'EcoReport_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        if st.button("🗑️ Reset Semua Data"):
            st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
            st.rerun()
    else:
        st.info("Lakukan perhitungan di setiap menu untuk mengumpulkan data laporan.")

# 6. KONTEN HALAMAN UTAMA

# --- 🏠 BERANDA ---
if page == "🏠 Beranda / Intro":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<h1 class="main-header">EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)
        st.write("### Solusi Engineering Pengolahan Air Limbah Terintegrasi")
        st.write("""
        Selamat datang profesional lingkungan! Platform ini dirancang untuk mempercepat alur kerja teknik Anda:
        - **Desain Unit:** Sizing bak pengolahan otomatis dengan visualisasi 3D.
        - **Kalkulasi Kimia:** Hitung kebutuhan koagulan secara stoikiometri.
        - **Analisis Kepatuhan:** Cek kualitas air terhadap standar baku mutu Permen LHK.
        """)
    with c2: st_lottie_embed(lottie_links["Intro"])

# --- 🏗️ UNIT SIZING ---
elif page == "🏗️ Unit Sizing":
    st.header("🏗️ Perancangan Dimensi Bak (Unit Sizing)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie_embed(lottie_links["Sizing"], height=150)
        q_in = st.number_input("Debit (m³/hari)", value=100.0, step=10.0)
        td_in = st.number_input("Waktu Tinggal (jam)", value=24.0, step=1.0)
        if st.button("💾 Proses & Simpan", type="primary", use_container_width=True):
            res = calculate_unit_sizing(q_in, td_in)
            st.session_state.sizing_res = res
            add_to_report('Unit Sizing', 'Debit', q_in, 'm3/hari')
                add_to_report('Unit Sizing', 'Dimensi (PxLxT)', f"{res['Panjang']}x{res['Lebar']}x{res['Tinggi']}3.5", 'meter')
    
    if 'sizing_res' in st.session_state:
        d = st.session_state.sizing_res
        with col2:
            st.markdown('<p class="sub-header">📐 Hasil Dimensi</p>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Volume", f"{d['Volume']} m³")
            m2.metric("Panjang", f"{d['Panjang']} m")
            m3.metric("Lebar", f"{d['Lebar']} m")
            
            fig = go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,3.5,3.5,3.5,3.5], color='#4CAF50', opacity=0.6)])
            fig.update_layout(scene=dict(xaxis_title='P', yaxis_title='L', zaxis_title='T'), margin=dict(l=0,r=0,b=0,t=0))
            st.plotly_chart(fig, use_container_width=True)

# --- 🧪 STOICHIOMETRY ---
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry (Kebutuhan Koagulan)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st_lottie_embed(lottie_links["Stoich"], height=150)
        bod_in = st.number_input("BOD Influen (mg/L)", value=200.0)
        q_val = st.number_input("Debit Operasional (m³/hari)", value=100.0)
        c_type = st.selectbox("Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("🧪 Hitung Dosis", use_container_width=True):
            dose = stoichiometry_coagulant(bod_in, q_val, c_type)
            st.session_state.stoich_res = {"val": dose, "type": c_type}
            add_to_report('Stoichiometry', f'Dosis {c_type}', dose, 'kg/hari')
    
    if 'stoich_res' in st.session_state:
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.write(f"### Kebutuhan {st.session_state.stoich_res['type']}")
            st.metric("Total Dosis", f"{st.session_state.stoich_res['val']} kg/hari")
            st.write("</div>", unsafe_allow_html=True)

# --- 📊 SIMULASI ---
elif page == "📊 Simulasi":
    st.header("📊 Simulasi Performa Pengolahan")
    c1, c2 = st.columns([1, 2])
    with c1:
        st_lottie_embed(lottie_links["Sim"], height=150)
        eff_val = st.slider("Efisiensi Penyisihan (%)", 50, 99, 85)
        bod_influent = st.number_input("BOD Masuk (mg/L)", value=200.0)
        bod_effluent = round(bod_influent * (1 - eff_val/100), 2)
        if st.button("📊 Simpan ke Report"):
            add_to_report('Simulasi', 'Estimasi Effluent', bod_effluent, 'mg/L')
            st.success("Tersimpan!")
    with c2:
        st.metric("Estimasi BOD Akhir", f"{bod_effluent} mg/L")
        st.bar_chart({'Influent (BOD)': bod_influent, 'Effluent (BOD)': bod_effluent})

# --- ✅ CHECKER ---
elif page == "✅ Checker":
    st.header("✅ Baku Mutu Compliance")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie_embed(lottie_links["Check"], height=150)
        b_e = st.number_input("BOD5", value=25.0); c_e = st.number_input("COD", value=80.0)
        t_e = st.number_input("TSS", value=20.0); p_e = st.number_input("pH", value=7.0)
        if st.button("🔍 Jalankan Verifikasi", type="primary", use_container_width=True):
            res_check = {'BOD5': b_e <= 30, 'COD': c_e <= 100, 'TSS': t_e <= 30, 'pH': 6 <= p_e <= 9}
            st.session_state.check_res = {"status": "LULUS" if all(res_check.values()) else "GAGAL", "details": res_check, "vals": [b_e, c_e, t_e, p_e]}
            add_to_report('Checker', 'Status Kepatuhan', st.session_state.check_res["status"], '-')

    if 'check_res' in st.session_state:
        with col2:
            st.markdown(f'<div class="metric-card"><h3>STATUS: {st.session_state.check_res["status"]}</h3></div>', unsafe_allow_html=True)
            st.table(pd.DataFrame({
                'Parameter': ['BOD5', 'COD', 'TSS', 'pH'],
                'Hasil': st.session_state.check_res["vals"],
                'Baku Mutu': [30, 100, 30, "6 - 9"],
                'Keterangan': ['✅' if v else '❌' for v in st.session_state.check_res["details"].values()]
            }))

# --- ℹ️ TENTANG WEB ---
elif page == "ℹ️ Tentang Web":
    st.header("ℹ️ Mengenai EcoEngineer Pro-Dash")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        **EcoEngineer Pro-Dash** adalah instrumen digital yang dirancang untuk mendukung pengambilan keputusan teknis di bidang teknik lingkungan.
        
        **Dasar Hukum & Teknis:**
        * **Regulasi:** Peraturan Menteri LHK No. P.68 Tahun 2016 tentang Baku Mutu Air Limbah Domestik.
        * **Metodologi Sizing:** Berdasarkan standar *Retention Time* dan *Surface Loading Rate* industri.
        * **Stoikiometri:** Didasarkan pada rasio teoritis penyisihan beban organik menggunakan koagulan kimia.
        
        **Tim Pengembang:** [Nama Anda / Tim Anda]
        **Versi:** 1.0 (Build 2026)
        """)
    with c2: st_lottie_embed(lottie_links["About"])

# 7. FOOTER
st.markdown(f'<div class="footer"><p>© {datetime.now().year} EcoEngineer Pro-Dash | Solusi Digital Untuk Lingkungan Berkelanjutan</p></div>', unsafe_allow_html=True)
