import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import io

# ==========================================
# 1. CONFIGURATION & PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="EcoEngineer Pro-Dash",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk memuat animasi Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animasi (Tema: Environment/Engineering)
lottie_eco = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_m9ubv9ts.json") # Animasi eco/pabrik bersih
lottie_loading = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_st966869.json")

# ==========================================
# 2. SIDEBAR - INPUT PARAMETER DATA
# ==========================================
with st.sidebar:
    st.markdown("## 📊 Data Karakteristik Limbah")
    
    # Input Debit
    Q_m3_day = st.number_input("Debit Air Limbah (Q) - m³/hari", min_value=1.0, value=500.0, step=10.0)
    Q_m3_hr = Q_m3_day / 24
    
    st.markdown("---")
    st.markdown("### 🧪 Konsentrasi Influent (Awal)")
    bod_in = st.number_input("BOD Influent (mg/L)", min_value=0.0, value=300.0, step=5.0)
    cod_in = st.number_input("COD Influent (mg/L)", min_value=0.0, value=600.0, step=10.0)
    tss_in = st.number_input("TSS Influent (mg/L)", min_value=0.0, value=250.0, step=5.0)
    
    st.markdown("---")
    st.markdown("### 📐 Parameter Desain Bak Pengendap (Sedimentasi)")
    td_hours = st.slider("Waktu Tinggal (td) - Jam", min_value=1.0, max_value=6.0, value=2.0, step=0.5)
    h_depth = st.slider("Kedalaman Efektif Bak (H) - Meter", min_value=1.5, max_value=5.0, value=3.0, step=0.1)
    w_to_l = st.slider("Rasio Lebar : Panjang (W:L)", min_value=0.1, max_value=1.0, value=0.33, step=0.05)

# ==========================================
# 3. MAIN DASHBOARD HEADER
# ==========================================
col_header_1, col_header_2 = st.columns([2, 1])

with col_header_1:
    st.title("🌱 EcoEngineer Pro-Dash")
    st.subheader("Desain Unit Pengolahan & Dashboard Kepatuhan Regulasi")
    st.markdown(
        "Aplikasi cerdas untuk melakukan otomatisasi dimensi unit IPAL, "
        "perhitungan stoikiometri koagulan, serta validasi baku mutu berdasarkan **PP No. 22 Tahun 2021**."
    )

with col_header_2:
    if lottie_eco:
        st_lottie(lottie_eco, height=180, key="eco_anim")

st.markdown("---")

# TABS UNTUK FITUR KOMPLEKS
tab1, tab2, tab3 = st.tabs(["📐 Automatic Sizing & Simulasi", "🧪 Stoichiometry Calculator", "📜 Regulatory Checker & Download Report"])

# ==========================================
# TAB 1: AUTOMATIC SIZING & SIMULATION
# ==========================================
with tab1:
    st.header("⚙️ Automatic Unit Sizing & Real-Time Simulation")
    
    # Perhitungan Sizing Mekanis
    volume_req = Q_m3_hr * td_hours
    surface_area = volume_req / h_depth
    
    # Menghitung Panjang (L) dan Lebar (W) berdasarkan rasio W/L
    # Area = L * W  --> Area = L * (L * rasio) --> L = sqrt(Area / rasio)
    length_bak = np.sqrt(surface_area / w_to_l)
    width_bak = length_bak * w_to_l
    overflow_rate = Q_m3_day / surface_area
    
    # Tampilan Hasil Sizing Metric
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Volume Bak Diperlukan", f"{volume_req:.2f} m³")
    col_m2.metric("Panjang Bak (L)", f"{length_bak:.2f} m")
    col_m3.metric("Lebar Bak (W)", f"{width_bak:.2f} m")
    col_m4.metric("Surface Overflow Rate", f"{overflow_rate:.2f} m³/m².hari")
    
    st.markdown("---")
    st.subheader("📈 Simulasi Interaktif Efisiensi Penyisihan (Removal Efficiency)")
    st.caption("Gunakan slider di bawah untuk mensimulasikan performa alat berdasarkan variasi efisiensi.")
    
    # Slider Simulasi Efisiensi
    col_sl1, col_sl2, col_sl3 = st.columns(3)
    with col_sl1:
        eff_bod = st.slider("Efisiensi Penyisihan BOD (%)", 50, 95, 85)
    with col_sl2:
        eff_cod = st.slider("Efisiensi Penyisihan COD (%)", 50, 95, 80)
    with col_sl3:
        eff_tss = st.slider("Efisiensi Penyisihan TSS (%)", 50, 99, 90)
        
    # Hitung Konsentrasi Effluent Hasil Simulasi
    bod_eff = bod_in * (1 - eff_bod/100)
    cod_eff = cod_in * (1 - eff_cod/100)
    tss_eff = tss_in * (1 - eff_tss/100)
    
    # Grafik Komparasi Menggunakan Plotly
    parameters = ['BOD', 'COD', 'TSS']
    influent_vals = [bod_in, cod_in, tss_in]
    effluent_vals = [bod_eff, cod_eff, tss_eff]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=parameters, y=influent_vals, name='Influent (Awal)', marker_color='#FFA07A'))
    fig.add_trace(go.Bar(x=parameters, y=effluent_vals, name='Effluent (Hasil Olahan)', marker_color='#20B2AA'))
    
    fig.update_layout(
        title_text='Perbandingan Konsentrasi Polutan (Influent vs Effluent)',
        barmode='group',
        xaxis_title='Parameter Kualitas Air',
        yaxis_title='Konsentrasi (mg/L)',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: STOICHIOMETRY CALCULATOR
# ==========================================
with tab2:
    st.header("🧪 Chemical Stoichiometry & Jar Test Scale-up")
    st.write("Hitung kebutuhan pasokan bahan kimia harian untuk proses koagulasi-flokulasi.")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("📥 Input Hasil Jar Test")
        jenis_koagulan = st.selectbox("Pilih Jenis Koagulan", ["Alum / Tawas (Al2(SO4)3)", "PAC (Polyaluminum Chloride)", "Fero Sulfat (FeSO4)"])
        dosis_jar = st.number_input("Dosis Optimum Hasil Jar Test (mg/L)", min_value=0.0, value=30.0, step=1.0)
        kemurnian = st.slider("Kemurnian Bahan Kimia Komersial (%)", 50, 100, 90)
        
    with col_c2:
        st.subheader("📊 Kebutuhan Bahan Kimia Harian")
        # Rumus: Kebutuhan (kg/hari) = (Q m3/hari * Dosis mg/L) / (1000 * (Kemurnian/100))
        # Karena 1 mg/L = 1 g/m3
        kebutuhan_murni = (Q_m3_day * dosis_jar) / 1000 # kg/hari
        kebutuhan_komersial = kebutuhan_murni / (kemurnian / 100)
        
        st.info(f"**Jenis Koagulan:** {jenis_koagulan}")
        st.metric("Kebutuhan Koagulan Murni", f"{kebutuhan_murni:.2f} kg/hari")
        st.metric("Kebutuhan Produk Komersial", f"{kebutuhan_komersial:.2f} kg/hari", 
                  help="Sudah memperhitungkan faktor kemurnian produk di pasar.")
        
        # Grafik Kebutuhan Bulanan (Proyeksi)
        hari = np.arange(1, 31)
        kumulatif_kimia = hari * kebutuhan_komersial
        
        fig_kimia = go.Figure()
        fig_kimia.add_trace(go.Scatter(x=hari, y=kumulatif_kimia, mode='lines+markers', name='Stok Koagulan', line=dict(color='#FF6347', width=2)))
        fig_kimia.update_layout(title='Proyeksi Konsumsi Kimia Bulanan (30 Hari)', xaxis_title='Hari ke-', yaxis_title='Total Akumulasi (kg)', template='plotly_white')
        st.plotly_chart(fig_kimia, use_container_width=True)

# ==========================================
# TAB 3: REGULATORY CHECKER & GABUNGAN DOWNLOAD
# ==========================================
with tab3:
    st.header("📜 Regulatory Compliance (PP No. 22 Tahun 2021)")
    st.write("Evaluasi otomatis kelayakan air limbah hasil olahan sebelum dilepas ke badan air lingkungan.")
    
    # Baku Mutu Domestik Umum berdasarkan Lampiran PP 22/2021 (atau Permen LHK 68/2016)
    BM_BOD = 30.0
    BM_COD = 100.0
    BM_TSS = 30.0
    
    # Cek Status Kepatuhan
    status_bod = "LULUS" if bod_eff <= BM_BOD else "GAGAL"
    status_cod = "LULUS" if cod_eff <= BM_COD else "GAGAL"
    status_tss = "LULUS" if tss_eff <= BM_TSS else "GAGAL"
    
    # Tampilkan Tabel Evaluasi Kepatuhan
    data_kepatuhan = {
        "Parameter": ["BOD", "COD", "TSS"],
        "Kadar Influent (mg/L)": [bod_in, cod_in, tss_in],
        "Hasil Olahan Effluent (mg/L)": [bod_eff, cod_eff, tss_eff],
        "Baku Mutu (mg/L)": [BM_BOD, BM_COD, BM_TSS],
        "Status Kelayakan": [status_bod, status_cod, status_tss]
    }
    
    df_kepatuhan = pd.DataFrame(data_kepatuhan)
    
    # Menggunakan Styler untuk memberikan warna background pada status Lulus/Gagal
    def color_status(val):
        color = '#2ecc71' if val == 'LULUS' else '#e74c3c'
        return f'background-color: {color}; color: white; font-weight: bold;'
    
    st.dataframe(df_kepatuhan.style.applymap(color_status, subset=['Status Kelayakan']), use_container_width=True)
    
    # Kesimpulan Akhir Sistem
    st.markdown("### 📢 Kesimpulan Akhir")
    if "GAGAL" in [status_bod, status_cod, status_tss]:
        st.error("❌ KESIMPULAN: Air limbah BELUM memenuhi standar baku mutu lingkungan. Tingkatkan efisiensi unit atau optimalkan dosis koagulan!")
        final_status = "BELUM MEMENUHI BAKU MUTU"
    else:
        st.success("✅ KESIMPULAN: Air limbah AMAN dan MEMENUHI standar regulasi untuk dibuang ke lingkungan.")
        final_status = "MEMENUHI BAKU MUTU"

    # ==========================================
    # FEATURE: DOWNLOAD CONSOLIDATED REPORT
    # ==========================================
    st.markdown("---")
    st.subheader("💾 Download Data Laporan Gabungan")
    st.write("Unduh semua ringkasan kalkulasi desain, stoikiometri, dan status regulasi dalam satu file data.")
    
    # Membuat struktur data gabungan untuk diekspor
    report_data = {
        "Kategori Parameter": [
            "Data Input", "Data Input", "Data Input", "Data Input",
            "Desain Sizing", "Desain Sizing", "Desain Sizing", "Desain Sizing",
            "Kimia & Stoikiometri", "Kimia & Stoikiometri", "Kimia & Stoikiometri",
            "Evaluasi Regulasi BOD", "Evaluasi Regulasi COD", "Evaluasi Regulasi TSS", "Kesimpulan Akhir"
        ],
        "Nama Komponen": [
            "Debit Limbah (Q)", "Influent BOD", "Influent COD", "Influent TSS",
            "Volume Bak Diperlukan", "Panjang Bak", "Lebar Bak", "Surface Overflow Rate",
            "Jenis Koagulan", "Dosis Optimal Jar Test", "Kebutuhan Produk Harian",
            f"Kadar Olahan vs Baku Mutu ({bod_eff:.1f}/{BM_BOD} mg/L)",
            f"Kadar Olahan vs Baku Mutu ({cod_eff:.1f}/{BM_COD} mg/L)",
            f"Kadar Olahan vs Baku Mutu ({tss_eff:.1f}/{BM_TSS} mg/L)",
            "Status Akhir IPAL"
        ],
        "Nilai / Output": [
            f"{Q_m3_day} m3/hari", f"{bod_in} mg/L", f"{cod_in} mg/L", f"{tss_in} mg/L",
            f"{volume_req:.2f} m3", f"{length_bak:.2f} m", f"{width_bak:.2f} m", f"{overflow_rate:.2f} m3/m2.hari",
            jenis_koagulan, f"{dosis_jar} mg/L", f"{kebutuhan_komersial:.2f} kg/hari",
            status_bod, status_cod, status_tss, final_status
        ]
    }
    
    df_report = pd.DataFrame(report_data)
    
    # Fungsi konversi ke CSV berformat bytes
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv_bytes = convert_df(df_report)
    
    # Tombol Download
    st.download_button(
        label="📥 Download Consolidated Engineering Report (.CSV)",
        data=csv_bytes,
        file_name='EcoEngineer_Pro_Dash_Report.csv',
        mime='text/csv',
    )

st.markdown("---")
st.caption("Developed by EcoEngineer Pro-Dash Team © 2026. Data validasi mengacu pada standar baku teknis air limbah nasional.")
