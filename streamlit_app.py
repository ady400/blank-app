import streamlit as st

# ==========================================
# CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="EcoWater COD Analyzer",
    page_icon="🌱",
    layout="centered",
)

# Custom CSS untuk UI Hijau yang Aesthetic
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f7f0;
    }
    h1, h2, h3 {
        color: #1b5e20 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 20px;
        border: none;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: #dcedc8;
    }
    .custom-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-top: 5px solid #4caf50;
        margin-bottom: 20px;
    }
    .formula-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border: 1px dashed #2e7d32;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/ecology-green-energy.png", width=80)
    st.title("Menu Utama")
    menu = st.radio(
        "Navigasi Halaman:",
        ["🏠 Beranda", "🧮 Kalkulator COD", "ℹ️ Tentang & Referensi"],
    )
    st.markdown("---")
    st.success("Status: Sistem Aktif 🟢")

# ==========================================
# HALAMAN 1: HOME (BERANDA)
# ==========================================
if menu == "🏠 Beranda":
    st.title("🌱 EcoWater COD Analyzer")
    
    # Foto Halaman Beranda
    st.image("https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1000&q=80", 
             caption="Melindungi sumber daya air untuk masa depan hijau.", use_column_width="always")
    
    st.markdown("""
    <div class="custom-card">
        <h3>Selamat Datang!</h3>
        <p><b>EcoWater COD Analyzer</b> adalah aplikasi berbasis web yang dirancang untuk membantu profesional lingkungan 
        menghitung kadar <i>Chemical Oxygen Demand</i> (COD) secara instan dan akurat.</p>
        <p>Aplikasi ini mengintegrasikan data laboratorium dengan standar regulasi pemerintah untuk memberikan analisis cepat 
        mengenai status kelayakan air limbah sebelum dilepas ke lingkungan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Akurasi", "99.9%")
    col2.metric("Kecepatan", "Instant")
    col3.metric("Standar", "SNI/LHK")

# ==========================================
# HALAMAN 2: KALKULATOR COD
# ==========================================
elif menu == "🧮 Kalkulator COD":
    st.title("🧮 Kalkulator Kadar COD")
    
    # Foto Halaman Kalkulator
    st.image("https://images.unsplash.com/photo-1581093588401-fbb62a02f120?auto=format&fit=crop&w=1000&q=80", 
             caption="Proses Titrasi Laboratorium untuk Penentuan Kadar COD.", use_column_width="always")

    # Bagian Rumus Perhitungan
    with st.expander("📝 Lihat Rumus Perhitungan (Metode Titrimetri)", expanded=True):
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.latex(r'''
            COD (mg/L) = \frac{(A - B) \times N \times 8000}{V_{sampel}}
        ''')
        st.markdown("""
        **Keterangan:**
        *   **A**: Volume penitar (FAS) untuk blanko (mL)
        *   **B**: Volume penitar (FAS) untuk sampel (mL)
        *   **N**: Normalitas larutan FAS (N)
        *   **8000**: Berat setara oksigen (mg/ekivalen)
        *   **V**: Volume sampel air yang diuji (mL)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Input Data
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📥 Data Hasil Uji")
        v_blanko = st.number_input("Volume Penitar Blanko (A)", min_value=0.0, value=10.0, step=0.1)
        v_sampel = st.number_input("Volume Penitar Sampel (B)", min_value=0.0, value=6.5, step=0.1)
        norm = st.number_input("Normalitas Penitar (N)", min_value=0.0, value=0.1, format="%.4f")
        v_air = st.number_input("Volume Sampel Air (mL)", min_value=1.0, value=25.0)
        
    with col_b:
        st.subheader("📋 Pilih Standar")
        st.write("Bandingkan hasil dengan Baku Mutu:")
        baku_opsi = {
            "Limbah Domestik (100 mg/L)": 100,
            "Industri Tekstil (150 mg/L)": 150,
            "Industri Cat (100 mg/L)": 100,
            "Custom Input": 0
        }
        pilihan = st.selectbox("Pilih Jenis Baku Mutu:", list(baku_opsi.keys()))
        
        if pilihan == "Custom Input":
            limit = st.number_input("Batas Maksimal (mg/L)", value=50)
        else:
            limit = baku_opsi[pilihan]
            st.info(f"Batas Maksimal: {limit} mg/L")

    # Tombol Hitung
    if st.button("🚀 HITUNG SEKARANG"):
        if v_blanko < v_sampel:
            st.warning("⚠️ Perhatian: Volume blanko biasanya lebih besar dari sampel. Pastikan data benar.")
        
        hasil = ((v_blanko - v_sampel) * norm * 8000) / v_air
        
        st.markdown("---")
        st.markdown(f"### Hasil Perhitungan: `{hasil:.2f} mg/L`")
        
        if hasil <= limit:
            st.success(f"✅ **LOLOS.** Kadar COD ({hasil:.2f}) memenuhi standar baku mutu ({limit}).")
            st.balloons()
        else:
            st.error(f"❌ **TIDAK LOLOS.** Kadar COD ({hasil:.2f}) melebihi batas aman ({limit}).")

# ==========================================
# HALAMAN 3: TENTANG APLIKASI
# ==========================================
elif menu == "ℹ️ Tentang & Referensi":
    st.title("ℹ️ Tentang Aplikasi")
    
    # Foto Halaman Tentang
    st.image("https://images.unsplash.com/photo-1542601906-990-b4d3fb778b09?auto=format&fit=crop&w=1000&q=80", 
             caption="Teknologi untuk Keberlanjutan Lingkungan.", use_column_width="always")

    col_dev, col_ref = st.columns(2)
    
    with col_dev:
        st.markdown("""
        <div class="custom-card">
            <h3>👤 Pembuat Aplikasi</h3>
            <p>Aplikasi ini dikembangkan oleh:</p>
            <ul>
                <li><b>Nama:</b> Raehan Ady Saesya</li>
                <li><b>Role:</b> Developer & Environmental Analyst</li>
                <li><b>Tujuan:</b> Alat bantu praktikum & monitoring IPAL.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ref:
        st.markdown("""
        <div class="custom-card">
            <h3>📚 Referensi Utama</h3>
            <p>Metode perhitungan dan data baku
