import time
import numpy as np
import pandas as pd
import streamlit as st
import io
import requests
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# Fungsi untuk memuat animasi lottie dari URL dengan pengaman try-except
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Memuat Lottie animations
lottie_beranda = load_lottie_url("https://lottie.host/947d937e-1b76-43a0-b786-d255c0ee1e74/stE5uwmVhW.json")
lottie_lab = load_lottie_url("https://lottie.host/ad0ad4a2-3e19-4bc4-a8f8-6447dbc72c73/s5hNdaq1uX.json")
lottie_simulasi = load_lottie_url("https://lottie.host/452e722c-e5f7-4a5a-bdaa-4f46c93a4ee6/FlkgyfRxKz.json")
lottie_proses = load_lottie_url("https://lottie.host/83a75fcc-2836-4020-ba68-10b9e0f7aa75/RTuEA9yHNB.json")
lottie_edukasi = load_lottie_url("https://lottie.host/30b3a6b0-a898-4862-a498-5600b93ee6a7/R9YyJLBYSA.json")
lottie_laboratorium = load_lottie_url("https://lottie.host/512b24b7-72c0-4868-93cf-641162ab8ce5/y2TUFxINa1.json")
lottie_interaktif = load_lottie_url("https://lottie.host/05ce74d8-a548-48b4-9dd0-04ec7c20bec1/gKJaJSYHw1.json")
lottie_sidebar = load_lottie_url("https://lottie.host/46d5d5e6-71ac-47f0-b042-9d7bece4d120/KUFhym6hHY.json")
lottie_tentang = load_lottie_url("https://lottie.host/2ca14505-599f-44fc-9516-fa2213084686/vW634tXhdC.json")

# Konfigurasi halaman
st.set_page_config(page_title="Limbah Track", page_icon="♻️", layout="wide")

# Sidebar
with st.sidebar:
    if lottie_sidebar:
        st_lottie(lottie_sidebar, speed=1, quality="high", height=150, key="sidebar_anim")
    st.title("♻️ Limbah Track")
    st.markdown("Belajar & Simulasi Pengolahan Limbah Industri 🌍")
    st.markdown("---")
    menu = st.radio("Navigasi", ["🏠 Beranda", "⚙️ Proses", "🧪 Uji Lab", "🧩 Konsentrasi", "ℹ️ Tentang"])
    st.markdown("---")
    st.caption("© 2026 Kelompok 6 - 1F PLI AKA")

# CSS tambahan buat mempercantik
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #2C3E50;
        text-align: center;
        padding: 20px 0;
    }
    .stButton>button {
        background-color: #2C3E50;
        color: white;
    }
    body {
        background-color: #f5f9ff;
    }
    </style>
""", unsafe_allow_html=True)

# BERANDA
if menu == "🏠 Beranda":
    if lottie_beranda:
        st_lottie(lottie_beranda, speed=1, quality="high", height=350, key="beranda_anim")
    st.markdown("""
        <style>
        .hero {
            background: linear-gradient(135deg, #d4edda, green);
            color: white;
            padding: 40px 20px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
        <div class='hero'>
            <h1>♻️ Manajemen & Edukasi Limbah Industri ♻️</h1>
            <p>Belajar dan menghitung bagaimana pengolahan limbah industri secara baku mutu.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if lottie_edukasi:
            st_lottie(lottie_edukasi, speed=1, quality="high", height=150, key="edu_anim")
        st.markdown("### Edukasi Proses")
        st.write("Kenali tahapan proses pemisahan pengolahan limbah dari awal.")
    with col2:
        if lottie_laboratorium:
            st_lottie(lottie_laboratorium, speed=1, quality="high", height=150, key="lab_anim_home")
        st.markdown("### Uji Laboratorium")
        st.write("Hitung nilai COD, BOD, TSS, dan pH dari data sampel.")
    with col3:
        if lottie_interaktif:
            st_lottie(lottie_interaktif, speed=1, quality="high", height=150, key="interaktif_anim")
        st.markdown("### Perhitungan Simulasi")
        st.write("Lakukan perhitungan kadar limbah yang bisa dibuang sesuai baku mutu.")

# PROSES
elif menu == "⚙️ Proses":
    if lottie_proses:
        st_lottie(lottie_proses, speed=1, quality="high", height=200, key="proses_anim")
    st.markdown('<div class="main-title">⚙️ Tahapan Pengolahan Limbah Industri</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 🧹 1. Pra-Pengolahan (Pre-Treatment)
    - **Screening:** Menyaring benda kasar seperti plastik dan kayu.
    - **Grit Chamber:** Mengendapkan partikel berat seperti pasir.
    - **Equalization Tank:** Menyeimbangkan aliran dan beban limbah.

    ### 🧪 2. Pengolahan Primer
    - **Primary Clarifier:** Mengendapkan padatan tersuspensi.

    ### 🧬 3. Pengolahan Sekunder (Biologis)
    - **Aerob:** Dengan oksigen (activated sludge, trickling filter).
    - **Anaerob:** Tanpa oksigen untuk limbah berat.

    ### 🧼 4. Pengolahan Tersier
    - **Filtrasi, Reverse Osmosis, Proses Kimia.**

    ### 🧱 5. Pengolahan Lumpur
    - **Thickening, Digestion, Dewatering.**

    ### 🌊 6. Pembuangan Akhir
    - **Limbah cair buangan yang memenuhi standar.**
    """)

# UJI LAB
elif menu == "🧪 Uji Lab":
    if lottie_lab:
        st_lottie(lottie_lab, speed=1, quality="high", height=200, key="lab_calc_anim")
    st.markdown('<div class="main-title">🧪 Kalkulator Uji Laboratorium</div>', unsafe_allow_html=True)
    uji = st.selectbox("Pilih jenis uji:", ["COD", "BOD", "TSS", "pH"])

    if uji == "COD":
        st.markdown("### Rumus Umum COD:")
        st.latex(r'''\text{COD (mg/L)} = \frac{(V_b - V_s) \times N \times 8000}{V_{\text{sampel}}}''')

        st.markdown("""
            **Keterangan:** - $V_b$ : Volume titran untuk blanko (mL)  
            - $V_s$ : Volume titran untuk sampel (mL)  
            - $N$ : Normalitas (N)  
            - $V_{\text{sampel}}$ : Volume sampel (mL)  
            """)
        
        # Perbaikan Input Variabel agar sinkron dengan rumus asli
        vb = st.number_input("Volume titran Blanko / Vb (mL)", value=12.0)
        vs_titran = st.number_input("Volume titran Sampel / Vs (mL)", value=10.0)
        n = st.number_input("Normalitas FAS / N (N)", value=0.1)
        v_sampel = st.number_input("Volume sampel / Vsampel (mL)", value=50.0)
        
        if st.button("Hitung COD"):
            if vb >= vs_titran:
                hasil = ((vb - vs_titran) * n * 8000) / v_sampel
                st.success(f"COD = {hasil:.2f} mg/L")

                fig = go.Figure(data=[go.Pie(
                    labels=["COD", "Sisa Kapasitas Oksigen"],
                    values=[hasil, max(500 - hasil, 0)],
                    hole=0.5,
                    marker_colors=["#2C3E50", "#95a5a6"]
                )])
                fig.update_layout(width=400, height=300)
                st.plotly_chart(fig)

                buffer = io.StringIO()
                buffer.write(f"Hasil Uji COD\nVol Blanko: {vb} mL\nVol Sampel Titran: {vs_titran} mL\nNormalitas: {n} N\nVol Sampel Air: {v_sampel} mL\n=> COD = {hasil:.2f} mg/L")
                st.download_button("📄 Unduh Hasil", buffer.getvalue(), file_name="hasil_uji_cod.txt")
            else:
                st.error("Volume Blanko (Vb) harus lebih besar atau sama dengan Volume Sampel (Vs)!")

    elif uji == "BOD":
        st.markdown("### Rumus Umum BOD:")
        st.latex(r'''\text{BOD (mg/L)} = D_1 - D_2''')

        st.markdown("""
            **Keterangan:** - $D_1$ : Konsentrasi DO awal (sebelum inkubasi)  
            - $D_2$ : Konsentrasi DO akhir (setelah inkubasi 5 hari)  
            """)
        
        awal = st.number_input("DO Awal (mg/L)", value=8.0)
        akhir = st.number_input("DO Akhir (mg/L)", value=2.0)
        if st.button("Hitung BOD"):
            hasil = awal - akhir
            st.success(f"BOD = {hasil:.2f} mg/L")

            fig = go.Figure(data=[go.Pie(
                labels=["Terpakai (BOD)", "Tersisa (Oksigen)"],
                values=[hasil, akhir],
                hole=0.5,
                marker_colors=["#3498db", "#ecf0f1"]
            )])
            fig.update_layout(width=400, height=300)
            st.plotly_chart(fig)

            buffer = io.StringIO()
            buffer.write(f"Hasil Uji BOD\nDO Awal: {awal} mg/L\nDO Akhir: {akhir} mg/L\n=> BOD = {hasil:.2f} mg/L")
            st.download_button("📄 Unduh Hasil", buffer.getvalue(), file_name="hasil_uji_bod.txt")

    elif uji == "TSS":
        st.markdown("### Rumus TSS:")
        st.latex(r'''\text{TSS (mg/L)} = \frac{(W_2 - W_1) \times 1000}{V}''')

        st.markdown("""
            **Keterangan:** - $W_1$ : Berat kertas saring kosong (mg)  
            - $W_2$ : Berat kertas saring + padatan kering (mg)  
            - $V$ : Volume sampel air (L)  
            """)
        awal = st.number_input("Berat filter awal (mg)", value=100.0)
        akhir = st.number_input("Berat filter akhir (mg)", value=120.0)
        volume = st.number_input("Volume sampel (L)", value=1.0)
        if st.button("Hitung TSS"):
            hasil = (akhir - awal) / volume
            st.success(f"TSS = {hasil:.2f} mg/L")

            fig = go.Figure(data=[go.Pie(
                labels=["Padatan Tersuspensi", "Lainnya"],
                values=[hasil, max(100 - hasil, 0)],
                hole=0.5,
                marker_colors=["#9b59b6", "#dcdde1"]
            )])
            fig.update_layout(width=400, height=300)
            st.plotly_chart(fig)

            buffer = io.StringIO()
            buffer.write(f"Hasil Uji TSS\nBerat awal: {awal} mg\nBerat akhir: {akhir} mg\nVolume: {volume} L\n=> TSS = {hasil:.2f} mg/L")
            st.download_button("📄 Unduh Hasil", buffer.getvalue(), file_name="hasil_uji_tss.txt")

    elif uji == "pH":
        ph = st.slider("pH sampel", 0.0, 14.0, 7.0)
        st.info(f"pH = {ph}")
        warna = "#2ecc71" if 6.0 <= ph <= 9.0 else "#e74c3c" # Menyesuaikan rentang standar air limbah
        fig = go.Figure(data=[go.Pie(
            labels=["pH", "Skala Tersisa"],
            values=[ph, 14 - ph],
            hole=0.5,
            marker_colors=[warna, "#ecf0f1"]
        )])
        fig.update_layout(width=400, height=300)
        st.plotly_chart(fig)

# SIMULASI KONSENTRASI
elif menu == "🧩 Konsentrasi":
    if lottie_simulasi:
        st_lottie(lottie_simulasi, speed=1, quality="high", height=200, key="sim_kons_anim")
    st.markdown('<div class="main-title">🧩 Perhitungan Konsentrasi Limbah</div>', unsafe_allow_html=True)

    st.markdown("### Rumus Pengurangan Konsentrasi Limbah:")
    st.latex(r'''C_{\text{akhir}} = C_{\text{awal}} \times (1 - \text{efisiensi})''')
    st.markdown("""
    **Keterangan:** - $C_{\text{awal}}$ : Konsentrasi awal limbah (mg/L)  
    - $\text{efisiensi}$ : Efisiensi pengolahan limbah (%)  
    - $C_{\text{akhir}}$ : Konsentrasi limbah setelah pengolahan (mg/L)  
    """)
    
    jenis = st.selectbox("Jenis limbah", ["Kimia", "Organik", "Campuran"])
    awal = st.number_input("Konsentrasi awal (mg/L)", value=500.0)

    # PERBAIKAN: Nilai efisiensi disesuaikan tepat dengan catatan kaki (Kimia 80%, Organik 70%, Campuran 60%)
    efisiensi = {"Kimia": 0.80, "Organik": 0.70, "Campuran": 0.60}[jenis]
    
    if st.button("Mulai Simulasi"):
        akhir = awal * (1 - efisiensi)
        st.success(f"Hasil akhir setelah pengolahan: {akhir:.2f} mg/L ({efisiensi*100:.0f}% efisiensi)")

        fig = go.Figure(data=[go.Pie(
            labels=["Terolah (Efisiensi)", "Sisa Emisi"],
            values=[awal - akhir, akhir],
            hole=0.5,
            marker_colors=["#27ae60", "#e74c3c"]
        )])
        fig.update_layout(width=400, height=300)
        st.plotly_chart(fig)

        buffer = io.StringIO()
        buffer.write(f"Simulasi Pengolahan Limbah\nJenis: {jenis}\nKonsentrasi awal: {awal} mg/L\nEfisiensi: {efisiensi*100:.0f}%\n=> Hasil akhir: {akhir:.2f} mg/L")
        st.download_button("📄 Unduh Hasil", buffer.getvalue(), file_name="hasil_simulasi.txt")
        
    st.markdown("---")
    st.caption("ℹ️ *Catatan: Nilai efisiensi simulasi (Kimia 80%, Organik 70%, dan Campuran 60%) disesuaikan dengan standar baku mutu PERMENLHK No. 5 Tahun 2014.*")
        
# TENTANG
elif menu == "ℹ️ Tentang":
    if lottie_tentang:
        st_lottie(lottie_tentang, speed=1, quality="high", height=150, key="about_page_anim")
    st.markdown('<div class="main-title">ℹ️ Tentang Aplikasi Ini</div>', unsafe_allow_html=True)
    st.write("""
    **Limbah Track** adalah aplikasi edukatif interaktif yang dirancang untuk membantu pengguna memahami proses dan perhitungan pengolahan limbah industri cair.

    Aplikasi ini menampilkan simulasi pengolahan, uji laboratorium, serta perhitungan parameter kualitas air limbah seperti:
    
    - **COD** (Chemical Oxygen Demand)
    - **BOD** (Biochemical Oxygen Demand)
    - **TSS** (Total Suspended Solid)
    - **pH** (derajat keasaman)

    ### 🎯 Tujuan:
    Membantu memahami batas baku mutu dan pentingnya pengolahan limbah cair industri agar tidak mencemari lingkungan.

    ### 📚 Referensi:
    - Modul Teknik Lingkungan
    - Litbang KLHK
    - **PERMENLHK No. 5 Tahun 2014** tentang Baku Mutu Air Limbah

    ### 👨‍💻 Teknologi:
    - Python + Streamlit
    - Visualisasi interaktif (Plotly, Lottie)

    ### 👥 Pengembang:
    - Kelompok 6 – 1F PLI AKA
    - Versi: 1.1 (2026)
    """)
