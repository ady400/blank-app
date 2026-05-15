import streamlit as st
import pd as pd
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime
import streamlit.components.v1 as components

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# Fungsi Animasi Lottie via HTML
def st_lottie_embed(url, height=200):
    embed_code = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center;">
        <lottie-player src="{url}" background="transparent" speed="1" style="width: {height}px; height: {height}px;" loop autoplay></lottie-player>
    </div>
    """
    return components.html(embed_code, height=height + 10)

lottie_links = {
    "Intro": "https://lottie.host/80516b34-897b-4029-8797-29007c570993/9nL0o0iYkS.json",
    "Sizing": "https://lottie.host/9e4871e9-4e08-466d-96f7-3c976f62664d/U0V166S04A.json",
    "Stoich": "https://lottie.host/318041c2-1925-4674-8d48-693175f0f353/Y9V4vXzT1j.json",
    "Check": "https://lottie.host/97f7429b-7561-4560-843c-6623e6179b9d/I8pB1X8E0A.json"
}

# 2. LOGIKA BACKEND
def calculate_unit_sizing(Q, td, H_input, SLR=24):
    V = Q * td / 24
    A = Q / SLR
    L = math.sqrt(A * 3)
    W = math.sqrt(A / 3)
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H_input}

def stoichiometry_coagulant(BOD_in, Q, coagulant_type):
    # Rasio dosis teoritis (mg koagulan / mg BOD penyisihan)
    ratios = {'FeCl3': 8.0, 'Alum': 10.0, 'PAC': 6.0}
    ratio = ratios.get(coagulant_type, 8.0)
    # Rumus: BOD (mg/L) * Debit (m3/hari) * Ratio / 1000 = kg/hari
    dosage = (BOD_in * Q * ratio) / 1000
    return round(dosage, 2)

# 3. STATE MANAGEMENT
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def add_to_report(cat, param, val, unit):
    new_entry = pd.DataFrame({'Kategori': [cat], 'Parameter': [param], 'Nilai': [val], 'Satuan': [unit]})
    st.session_state.full_report = pd.concat([st.session_state.full_report, new_entry], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 4. SIDEBAR
with st.sidebar:
    st_lottie_embed(lottie_links["Intro"], height=100)
    page = st.selectbox("Menu:", ["🏠 Beranda", "🏗️ Unit Sizing", "🧪 Stoichiometry", "✅ Checker", "ℹ️ Tentang"])
    
    st.divider()
    if not st.session_state.full_report.empty:
        csv_data = st.session_state.full_report.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Laporan (CSV)", data=csv_data, file_name="Report_Limbah.csv", use_container_width=True)

# 5. HALAMAN
if page == "🏠 Beranda":
    st.title("🌱 EcoEngineer Pro-Dash")
    st_lottie_embed(lottie_links["Intro"], height=300)
    st.write("Selamat datang! Gunakan menu di samping untuk mulai menghitung desain IPAL Anda.")

elif page == "🏗️ Unit Sizing":
    st.header("🏗️ Perancangan Dimensi Bak")
    c1, c2 = st.columns([1, 2])
    with c1:
        Q = st.number_input("Debit (m³/hari)", value=100.0)
        td = st.number_input("Retention Time (jam)", value=24.0)
        H_set = st.number_input("Tinggi Bak yang Diinginkan (m)", value=3.5, step=0.1) # INPUT TINGGI
        if st.button("Hitung & Simpan"):
            res = calculate_unit_sizing(Q, td, H_set)
            st.session_state.sizing_res = res
            add_to_report('Sizing', 'Dimensi (PxLxT)', f"{res['Panjang']}x{res['Lebar']}x{res['Tinggi']}", 'm')
    
    if 'sizing_res' in st.session_state:
        d = st.session_state.sizing_res
        with c2:
            st.metric("Volume Efektif", f"{d['Volume']} m³")
            st.write(f"**Dimensi:** {d['Panjang']}m (P) x {d['Lebar']}m (L) x {d['Tinggi']}m (T)")
            fig = go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,d['Tinggi'],d['Tinggi'],d['Tinggi'],d['Tinggi']], color='green', opacity=0.5)])
            st.plotly_chart(fig, use_container_width=True)

elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry (Kalkulator Koagulan)")
    st_lottie_embed(lottie_links["Stoich"], height=150)
    c1, c2 = st.columns(2)
    with c1:
        bod = st.number_input("BOD Influen (mg/L)", value=200.0)
        debit = st.number_input("Debit (m³/hari)", value=100.0)
        tipe = st.selectbox("Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("Hitung Dosis"):
            hasil = stoichiometry_coagulant(bod, debit, tipe)
            st.session_state.stoich_res = {"val": hasil, "type": tipe}
            add_to_report('Stoich', f'Dosis {tipe}', hasil, 'kg/hari')
            
    if 'stoich_res' in st.session_state:
        with c2:
            st.metric(f"Kebutuhan {st.session_state.stoich_res['type']}", f"{st.session_state.stoich_res['val']} kg/hari")
            st.info("Perhitungan berdasarkan beban organik (BOD) dikalikan rasio stoikiometri koagulan.")

elif page == "✅ Checker":
    st.header("✅ Baku Mutu Checker")
    st_lottie_embed(lottie_links["Check"], height=150)
    b = st.number_input("BOD5", value=25.0)
    c = st.number_input("COD", value=80.0)
    t = st.number_input("TSS", value=20.0)
    p = st.number_input("pH", value=7.0)
    if st.button("Cek Regulasi"):
        lulus = b <= 30 and c <= 100 and t <= 30 and 6 <= p <= 9
        status = "LULUS" if lulus else "GAGAL"
        st.subheader(f"Status: {status}")
        add_to_report('Checker', 'Status Kepatuhan', status, '-')

elif page == "ℹ️ Tentang":
    st.header("ℹ️ Informasi Aplikasi")
    st.write("**Referensi Utama:**")
    st.write("- Permen LHK No. P.68 Tahun 2016 (Baku Mutu Air Limbah)")
    st.write("- Metcalf & Eddy (Wastewater Engineering)")
