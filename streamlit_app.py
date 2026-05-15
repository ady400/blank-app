import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EcoEngineer Pro-Dash", page_icon="🌱", layout="wide")

# Fungsi Animasi Lottie via HTML (Anti-Error/Crash)
def st_lottie_embed(url, height=250):
    embed_code = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center;">
        <lottie-player src="{url}" background="transparent" speed="1" style="width: {height}px; height: {height}px;" loop autoplay></lottie-player>
    </div>
    """
    return components.html(embed_code, height=height + 10)

# Link Animasi
lottie_links = {
    "Intro": "https://lottie.host/80516b34-897b-4029-8797-29007c570993/9nL0o0iYkS.json",
    "Sizing": "https://lottie.host/9e4871e9-4e08-466d-96f7-3c976f62664d/U0V166S04A.json",
    "About": "https://lottie.host/7e0c4f1c-d72b-4b11-9721-657d90e0e01c/v6W70M7u5I.json"
}

# 2. Styling CSS
st.markdown("""
<style>
.main-header {font-size: 2.8rem; color: #2E7D32; font-weight: bold;}
.metric-card {background-color: #F1F8E9; padding: 1.5rem; border-radius: 12px; border-left: 6px solid #4CAF50; margin-bottom: 1rem;}
.footer {text-align: center; margin-top: 50px; color: #757575; border-top: 1px solid #eee; padding-top: 20px;}
.stButton>button {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# 3. Logika Backend
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9)}

def calculate_unit_sizing(Q, td, SLR=24):
    V, A = (Q * td / 24), (Q / SLR)
    L, W, H = math.sqrt(A * 3), math.sqrt(A / 3), 3.5
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

# 4. State Management (Penting agar data download tidak hilang)
if 'full_report' not in st.session_state:
    st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])

def update_report(df_new):
    st.session_state.full_report = pd.concat([st.session_state.full_report, df_new], ignore_index=True).drop_duplicates(subset=['Kategori', 'Parameter'], keep='last')

# 5. Sidebar & Fitur Download
with st.sidebar:
    st_lottie_embed(lottie_links["Intro"], height=120)
    st.title("🌱 EcoEngineer")
    page = st.selectbox("Navigasi Halaman:", ["🏠 Beranda", "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi", "✅ Checker", "ℹ️ Tentang Aplikasi"])
    
    st.divider()
    st.subheader("📥 Export Data")
    if not st.session_state.full_report.empty:
        # Pembuatan Laporan CSV yang Rapi
        header_text = [
            ["LAPORAN HASIL PENGUKURAN ECOENGINEER PRO-DASH", "", "", ""],
            [f"Waktu Generate: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "", "", ""],
            ["Status: Dokumen Teknis Digital", "", "", ""],
            ["="*45, "="*20, "="*20, "="*10],
            ["KATEGORI", "PARAMETER", "NILAI", "SATUAN"]
        ]
        header_df = pd.DataFrame(header_text, columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
        final_download_df = pd.concat([header_df, st.session_state.full_report], ignore_index=True)
        
        st.download_button(
            label="Download Full Report (CSV)",
            data=final_download_df.to_csv(index=False, header=False).encode('utf-8'),
            file_name=f'Report_EcoEngineer_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        if st.button("🗑️ Reset Data", use_container_width=True):
            st.session_state.full_report = pd.DataFrame(columns=['Kategori', 'Parameter', 'Nilai', 'Satuan'])
            st.rerun()
    else:
        st.info("Belum ada data untuk didownload. Lakukan perhitungan terlebih dahulu.")

# 6. Konten Halaman

if page == "🏠 Beranda":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<h1 class="main-header">EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)
        st.write("### Smart Solution for Wastewater Engineering")
        st.write("Platform integratif untuk mempermudah tugas Insinyur Lingkungan dalam perancangan IPAL, perhitungan kimia, dan monitoring regulasi dalam satu genggaman.")
    with c2: st_lottie_embed(lottie_links["Intro"])

elif page == "🏗️ Unit Sizing":
    st.header("🏗️ Unit Sizing (Dimensi Bak)")
    col1, col2 = st.columns([1, 1])
    with col1:
        Q = st.number_input("Debit Limbah (m³/hari)", value=100.0)
        td = st.number_input("Retention Time (jam)", value=24.0)
        if st.button("Hitung Dimensi", type="primary"):
            d = calculate_unit_sizing(Q, td)
            st.session_state.last_dims = d
            update_report(pd.DataFrame({'Kategori':['Sizing']*3, 'Parameter':['Volume','Luas','Dimensi PxL'], 'Nilai':[d['Volume'], d['Luas'], f"{d['Panjang']}x{d['Lebar']}"], 'Satuan':['m3','m2','m']}))
    
    if 'last_dims' in st.session_state:
        d = st.session_state.last_dims
        with col2:
            st.metric("Volume Efektif", f"{d['Volume']} m³")
            st.write(f"**Dimensi Rekomendasi:** {d['Panjang']}m (P) x {d['Lebar']}m (L) x 3.5m (T)")
            fig = go.Figure(data=[go.Mesh3d(x=[0,d['Panjang'],d['Panjang'],0,0,d['Panjang'],d['Panjang'],0], y=[0,0,d['Lebar'],d['Lebar'],0,0,d['Lebar'],d['Lebar']], z=[0,0,0,0,3.5,3.5,3.5,3.5], color='green', opacity=0.5)])
            st.plotly_chart(fig, use_container_width=True)

elif page == "ℹ️ Tentang Aplikasi":
    st.header("ℹ️ Tentang EcoEngineer Pro-Dash")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        **Visi Aplikasi:**
        Mendigitalisasi perhitungan teknik lingkungan agar lebih cepat, akurat, dan terdokumentasi dengan baik. 
        
        **Dasar Perhitungan & Referensi:**
        1. **Permen LHK No. P.68/2016:** Standar Baku Mutu Air Limbah Domestik.
        2. **Metcalf & Eddy:** Prinsip dasar Wastewater Engineering (Sizing & Stoichiometry).
        3. **SNI 6774:2008:** Tata cara perencanaan unit paket instalasi pengolahan air.
        
        **Pengembang:**
        Dibuat oleh Tim EcoEngineer untuk komunitas Insinyur Lingkungan Indonesia.
        """)
    with c2:
        st_lottie_embed(lottie_links["About"])

# Fitur Stoichiometry, Simulasi, dan Checker tetap ada (Sama dengan versi sebelumnya)
# [BAGIAN INI TETAP UTUH SEPERTI KODE SEBELUMNYA AGAR TIDAK ADA YANG ILANG]
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry")
    b_in = st.number_input("BOD Masuk (mg/L)", value=200.0)
    q_s = st.number_input("Debit (m³/hari)", value=100.0)
    coag = st.selectbox("Koagulan", ['FeCl3', 'Alum', 'PAC'])
    if st.button("Hitung Kebutuhan"):
        ratios = {'FeCl3': 8, 'Alum': 10, 'PAC': 6}
        res = round(b_in * ratios.get(coag) * q_s / 1000, 2)
        st.metric(f"Kebutuhan {coag}", f"{res} kg/hari")
        update_report(pd.DataFrame({'Kategori':['Stoich'], 'Parameter':[f'Dosis {coag}'], 'Nilai':[res], 'Satuan':['kg/hari']}))

elif page == "📊 Simulasi":
    st.header("📊 Simulasi Efisiensi")
    eff = st.slider("Efisiensi Alat (%)", 50, 99, 85)
    b_in_s = st.number_input("BOD Influent", value=200.0)
    b_out = round(b_in_s * (1 - eff/100), 2)
    st.metric("Estimasi Effluent", f"{b_out} mg/L")
    st.bar_chart({'In': b_in_s, 'Out': b_out})

elif page == "✅ Checker":
    st.header("✅ Baku Mutu Checker")
    val = {'BOD5': st.number_input("BOD5", 25.0), 'COD': st.number_input("COD", 80.0), 'TSS': st.number_input("TSS", 20.0), 'pH': st.number_input("pH", 7.0)}
    if st.button("Cek Sekarang"):
        res = {p: (val[p] <= BAKU_MUTU[p] if p != 'pH' else 6 <= val[p] <= 9) for p in val}
        status = "LULUS" if all(res.values()) else "GAGAL"
        st.markdown(f'<div class="metric-card"><h3>Hasil: {status}</h3></div>', unsafe_allow_html=True)
        update_report(pd.DataFrame({'Kategori':['Checker'], 'Parameter':['Status'], 'Nilai':[status], 'Satuan':['-']}))

# 7. Footer
st.markdown(f'<div class="footer"><p>© {datetime.now().year} EcoEngineer Pro-Dash | Built for Sustainability</p></div>', unsafe_allow_html=True)
