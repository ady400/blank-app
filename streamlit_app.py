import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime
import streamlit.components.v1 as components

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# Fungsi Animasi Lottie via HTML (Paling Aman, Tidak Bikin Error)
def st_lottie_embed(url, height=200):
    embed_code = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center;">
        <lottie-player src="{url}" background="transparent" speed="1" style="width: {height}px; height: {height}px;" loop autoplay></lottie-player>
    </div>
    """
    return components.html(embed_code, height=height + 10)

# Link Animasi yang Stabil
lottie_links = {
    "Intro": "https://lottie.host/80516b34-897b-4029-8797-29007c570993/9nL0o0iYkS.json",
    "Sizing": "https://lottie.host/9e4871e9-4e08-466d-96f7-3c976f62664d/U0V166S04A.json",
    "Stoich": "https://lottie.host/318041c2-1925-4674-8d48-693175f0f353/Y9V4vXzT1j.json",
    "Sim": "https://lottie.host/22b9f3d9-9520-4100-8802-5e3789431e56/m4a9xK8I0i.json",
    "Check": "https://lottie.host/97f7429b-7561-4560-843c-6623e6179b9d/I8pB1X8E0A.json",
    "About": "https://lottie.host/7e0c4f1c-d72b-4b11-9721-657d90e0e01c/v6W70M7u5I.json"
}

# 2. STYLING CSS
st.markdown("""
<style>
.main-header {font-size: 2.8rem; color: #2E7D32; font-weight: bold;}
.metric-card {background-color: #F1F8E9; padding: 1.5rem; border-radius: 12px; border-left: 6px solid #4CAF50; margin-bottom: 1rem;}
.footer {text-align: center; margin-top: 50px; color: #757575; border-top: 1px solid #eee; padding-top: 20px;}
</style>
""", unsafe_allow_html=True)

# 3. LOGIKA BACKEND & KONSTANTA
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9)}

def calculate_unit_sizing(Q, td, SLR=24):
    V, A = (Q * td / 24), (Q / SLR)
    L, W, H = math.sqrt(A * 3), math.sqrt(A / 3), 3.5
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

# 4. REPORT MANAGEMENT (Session State)
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. SIDEBAR NAVIGATION & DOWNLOAD
with st.sidebar:
    st_lottie_embed(lottie_links["Intro"], height=100)
    st.title("🌱 EcoEngineer Pro")
    page = st.selectbox("Menu Utama:", ["🏠 Beranda", "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker", "ℹ️ Tentang Aplikasi"])
    
    st.divider()
    st.subheader("📥 Download Report")
    if not st.session_state.full_report.empty:
        header_text = [
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Waktu Generate: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "", "", ""],
            ["Pembuat: [Nama Anda/Tim]", "", "", ""],
            ["="*45, "="*20, "="*20, "="*10],
            ["KATEGORI", "PARAMETER", "NILAI", "SATUAN"]
        ]
        header_df = pd.DataFrame(header_text, columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        final_download_df = pd.concat([header_df, st.session_state.full_report], ignore_index=True)
        
        st.download_button(
            label="Download Laporan (CSV)",
            data=final_download_df.to_csv(index=False, header=False).encode('utf-8'),
            file_name=f'Report_EcoEngineer_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        if st.button("🗑️ Reset Data"):
            st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
            st.rerun()
    else:
        st.info("Hitung data untuk ekspor.")

# 6. KONTEN HALAMAN

# --- 🏠 BERANDA ---
if page == "🏠 Beranda":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<h1 class="main-header">EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)
        st.write("### Smart Digital Platform for Wastewater Engineering")
        st.write("Solusi integratif untuk perancangan IPAL, perhitungan dosis kimia, dan verifikasi regulasi dalam satu platform.")
    with c2: st_lottie_embed(lottie_links["Intro"])

# --- 🏗️ UNIT SIZING ---
elif page == "🏗️ Unit Sizing":
    st.header("🏗️ Unit Sizing (Dimensi Bak)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie_embed(lottie_links["Sizing"], height=150)
        Q = st.number_input("Debit Air Limbah (m³/hari)", value=100.0)
        td = st.number_input("Retention Time (jam)", value=24.0)
        if st.button("💾 Hitung Dimensi", type="primary", use_container_width=True):
            d = calculate_unit_sizing(Q, td)
            st.session_state.last_dims = d
            update_report(pd.DataFrame({'Kategori':['Sizing']*3, 'Parameter':['Volume','Luas','Dimensi PxL'], 'Nilai':[d['Volume'], d['Luas'], f"{d['Panjang']}x{d['Lebar']}"], 'Satuan':['m3','m2','m']}))
    
    if 'last_dims' in st.session_state:
        with col2:
            d = st.session_state.last_dims
            st.subheader("📐 Hasil Perhitungan")
            m1, m2 = st.columns(2)
            m1.metric("Volume Efektif", f"{d['Volume']} m³")
            m2.metric("Luas Permukaan", f"{d['Luas']} m²")
            st.markdown(f"**Rekomendasi Dimensi (PxLxT):** \n### {d['Panjang']}m x {d['Lebar']}m x 3.5m")
            fig = go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,3.5,3.5,3.5,3.5], color='green', opacity=0.5)])
            st.plotly_chart(fig, use_container_width=True)

# --- 🧪 STOICHIOMETRY ---
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry (Kebutuhan Kimia)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st_lottie_embed(lottie_links["Stoich"], height=150)
        b_in = st.number_input("BOD Masuk (mg/L)", value=200.0)
        q_s = st.number_input("Debit (m³/hari)", value=100.0)
        coag = st.selectbox("Jenis Koagulan", ['FeCl3', 'Alum', 'PAC'])
        if st.button("🧪 Hitung Dosis", type="primary", use_container_width=True):
            ratios = {'FeCl3': 8, 'Alum': 10, 'PAC': 6}
            res = round(b_in * ratios.get(coag) * q_s / 1000, 2)
            st.session_state.last_stoich = {"val": res, "name": coag}
            update_report(pd.DataFrame({'Kategori':['Stoich'], 'Parameter':[f'Kebutuhan {coag}'], 'Nilai':[res], 'Satuan':['kg/hari']}))
    
    if 'last_stoich' in st.session_state:
        with col2:
            st.subheader("🧪 Hasil Dosis")
            st.metric(f"Kebutuhan {st.session_state.last_stoich['name']}", f"{st.session_state.last_stoich['val']} kg/hari")
            st.info("Dosis didasarkan pada rasio teoritis penyisihan BOD terhadap koagulan.")

# --- 📊 SIMULASI ---
elif page == "📊 Simulasi":
    st.header("📊 Simulasi Performa IPAL")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie_embed(lottie_links["Sim"], height=150)
        eff = st.slider("Efisiensi Alat (%)", 50, 99, 85)
        b_in_s = st.number_input("BOD Influent (mg/L)", value=200.0)
        if st.button("📊 Simpan Hasil", use_container_width=True):
            b_out = round(b_in_s * (1 - eff/100), 2)
            update_report(pd.DataFrame({'Kategori':['Simulasi'], 'Parameter':['BOD Effluent'], 'Nilai':[b_out], 'Satuan':['mg/L']}))
            st.success("Tersimpan!")
    with col2:
        b_out = round(b_in_s * (1 - eff/100), 2)
        st.metric("Estimasi BOD Keluar", f"{b_out} mg/L")
        st.bar_chart({'In (BOD)': b_in_s, 'Out (BOD)': b_out})

# --- ✅ CHECKER ---
elif page == "✅ Checker":
    st.header("✅ Regulatory Checker")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie_embed(lottie_links["Check"], height=150)
        b_e = st.number_input("BOD5", value=25.0)
        c_e = st.number_input("COD", value=80.0)
        t_e = st.number_input("TSS", value=20.0)
        p_e = st.number_input("pH", value=7.0)
    
    if st.button("🔍 Jalankan Cek Kepatuhan", type="primary", use_container_width=True):
        res = {'BOD5': b_e <= 30, 'COD': c_e <= 100, 'TSS': t_e <= 30, 'pH': 6 <= p_e <= 9}
        status = "LULUS" if all(res.values()) else "GAGAL"
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Status Akhir: {status}</h3></div>', unsafe_allow_html=True)
            st.table(pd.DataFrame({'Parameter': res.keys(), 'Nilai': [b_e, c_e, t_e, p_e], 'Status': ['✅ OK' if v else '❌ Melebihi' for v in res.values()]}))
            update_report(pd.DataFrame({'Kategori':['Checker'], 'Parameter':['Kepatuhan'], 'Nilai':[status], 'Satuan':['-']}))

# --- ℹ️ TENTANG APLIKASI ---
elif page == "ℹ️ Tentang Aplikasi":
    st.header("ℹ️ Mengenai Platform")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        **EcoEngineer Pro-Dash** dikembangkan untuk standarisasi perhitungan teknis lingkungan.
        
        **Referensi Teknis:**
        * **Permen LHK P.68/2016:** Standar Baku Mutu Air Limbah.
        * **Metcalf & Eddy:** Wastewater Engineering: Treatment and Resource Recovery.
        * **SNI 6774:2008:** Tata cara perencanaan unit paket IPAL.
        """)
    with c2: st_lottie_embed(lottie_links["About"])

# 7. FOOTER
st.markdown(f'<div class="footer"><p>© {datetime.now().year} EcoEngineer Pro-Dash | Built for Sustainability</p></div>', unsafe_allow_html=True)
