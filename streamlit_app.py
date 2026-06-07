import streamlit as st

# ==========================================
# CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="EcoWater COD Analyzer",
    page_icon="🌱",
    layout="centered",
)

# Custom CSS Global untuk mempercantik UI & komponen internal
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
    }
    section[data-testid="stSidebar"] {
        background-color: #f0fdf4 !important;
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #334155 !important;
    }
    div.stButton > button:first-child {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #059669;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* 1. KODE UNTUK MEMBUAT FOTO OTOMATIS DI TENGAH DAN TIDAK ZOOM */
    .stApp img {
        max-width: 65% !important; /* Batasi lebar foto agar tidak terlalu besar */
        height: auto !important;    /* Rasio foto tetap proporsional */
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 15px;       /* Sudut melengkung halus */
    }
    
    /* Khusus untuk logo kecil di dalam sidebar agar tidak ikut ke tengah */
    section[data-testid="stSidebar"] img {
        max-width: 100% !important;
        display: inline-block !important;
    }

    /* 2. KODE BARU: MEMBUAT SEMUA JUDUL UTAMA DAN SUB-JUDUL DI TENGAH SECARA GLOBAL */
    .stApp h1, .stApp h2, .stApp h3, .stApp p[style*="text-align: center"] {
        text-align: center !important;
    }
    
    /* Membuat blok text deskripsi bawaan menu ikut rapi di tengah */
    div[data-testid="stMarkdownContainer"] > div[style*="max-width: 800px"] {
        margin: 0 auto !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* 1. KODE UNTUK FOTO DI HALAMAN UTAMA (BERANDA) AGAR DI TENGAH */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    [data-testid="stImage"] img {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 12px; /* Membuat sudut foto melengkung rapi seperti di gambarmu */
    }

    /* 2. KODE KHUSUS UNTUK FOTO DI DALAM SIDEBAR (FOTO ERLENMEYER) */
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stImage"] img {
        max-width: 180px !important; /* Batasi ukuran foto di sidebar agar proporsional */
        height: auto !important;
    }

    /* 3. KODE AGAR TABEL DATAFRAME JUGA IKUT DI TENGAH HALAMAN */
    [data-testid="stDataFrame"] {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://i.pinimg.com/736x/a0/92/58/a09258df83907bc5d1f8f506a037cd76.jpg", width=100)
    st.title("EcoWater")
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
    st.markdown("<h1 style='text-align: center; color: #047857; font-weight: 800; margin-bottom: 20px;'>🌱 EcoWater COD Analyzer</h1>", unsafe_allow_html=True)
    
    # Foto Halaman Beranda
    st.image("https://i.pinimg.com/1200x/48/81/54/4881545ab4580b32e5bb0ce8679b8598.jpg", 
             caption="Melindungi sumber daya air untuk masa depan hijau.", use_column_width="always")
    
    st.markdown("""
    <div class="custom-card">
        <h3>Selamat Datang</h3>
        <p><b>EcoWater COD Analyzer</b> adalah aplikasi berbasis web yang dirancang untuk membantu profesional lingkungan 
        menghitung kadar <i>Chemical Oxygen Demand</i> (COD) secara instan dan akurat.</p>
        <p>Aplikasi ini mengintegrasikan data laboratorium dengan standar regulasi pemerintah untuk memberikan analisis cepat 
        mengenai status kelayakan air limbah sebelum dilepas ke lingkungan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Membuat 3 kolom untuk box HTML
    box_col1, box_col2, box_col3 = st.columns(3)
    
    with box_col1:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #10b981; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">AKURASI ANALISIS</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">99.9%</span>
            </div>
        """, unsafe_allow_html=True)
    
    with box_col2:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #3b82f6; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">KECEPATAN RESPON</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">Instant</span>
            </div>
        """, unsafe_allow_html=True)
    
    with box_col3:
        st.markdown("""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #f59e0b; text-align: center;">
                <span style="font-size: 14px; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">STANDAR ACUAN</span><br>
                <span style="font-size: 28px; font-weight: 800; color: #1e293b; display: block; margin-top: 5px;">SNI / LHK</span>
            </div>
        """, unsafe_allow_html=True)
# ==========================================
# HALAMAN 2: KALKULATOR COD
# ==========================================
elif menu == "🧮 Kalkulator COD":
    st.title("Kalkulator Kadar COD")
    
    # Foto Halaman Kalkulator
    st.image("https://i.pinimg.com/736x/2d/f4/4c/2df44ccf0de9728ae2ba1f623cf3a937.jpg", 
             caption="Proses Titrasi Laboratorium untuk Penentuan Kadar COD.", use_column_width="always")

    # Bagian Rumus Perhitungan
    # Pastikan menggunakan struktur 'with st.expander' seperti ini:
    with st.expander("Rumus Perhitungan (Metode Titrimetri)"):
        
        # 1. Tampilkan rumus utama (Gunakan objek st.latex agar rapi di tengah)
        st.latex(r"COD (mg/L) = \frac{(A - B) \times N \times 8000}{V_{sampel}}")
        
        # 2. Tampilkan keterangan komponen rumus
        st.markdown("""
        **Keterangan:**
        * **A:** Volume penitar (FAS) untuk blanko (mL)
        * **B:** Volume penitar (FAS) untuk sampel (mL)
        * **N:** Normalitas larutan FAS (N)
        * **8000:** Berat setara oksigen (mg/ekivalen)
        * **V:** Volume sampel air yang diuji (mL)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Input Data
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📥 Data Hasil Uji")
        v_blanko = st.number_input("Volume Penitar Blanko (A)", min_value=0.0, value=10.0, step=0.1)
        v_sampel = st.number_input("Volume Penitar Sampel (B)", min_value=0.0, value=6.5, step=0.1)
        norm = st.number_input("Normalitas Penitar (N)", min_value=0.0000, value=0.1000, format="%.4f", step=0.001)
        v_air = st.number_input("Volume Sampel Air (mL)", min_value=1.0, value=25.0, step=1.0)
        
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
            st.success(f"✅ **LOLOS.** Kadar COD ({hasil:.2f} mg/L) memenuhi standar baku mutu ({limit} mg/L).")
            st.balloons()
        else:
            st.error(f"❌ **TIDAK LOLOS.** Kadar COD ({hasil:.2f} mg/L) melebihi batas aman ({limit} mg/L).")

# ==========================================
# HALAMAN 3: TENTANG APLIKASI
# ==========================================
elif menu == "ℹ️ Tentang & Referensi":
    st.title("Tentang Aplikasi")
    
    # Foto Halaman Tentang
    st.image("https://i.pinimg.com/1200x/80/e5/df/80e5df94c2c611c566909ad629a86cd8.jpg", 
             caption="Teknologi untuk Keberlanjutan Lingkungan.", use_column_width="always")

    col_dev, col_ref = st.columns(2)
    
    with col_dev:
        st.markdown("""
        <div class="custom-card">
            <h3>👤 Pembuat Aplikasi</h3>
            <p>Aplikasi ini dikembangkan oleh:</p>
            <ul>
                <li><b>Nama:</b> Kelompok</li>
                <li><b>Role:</b> Developer & Environmental Analyst</li>
                <li><b>Tujuan:</b> Alat bantu praktikum & monitoring IPAL</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ref:
        st.markdown("""
        <div class="custom-card">
            <h3>📚 Referensi Utama</h3>
            <p>Metode perhitungan dan data baku mutu didasarkan pada:</p>
            <ol>
                <li><b>SNI 6989.2:2019</b> (Cara Uji COD)</li>
                <li><b>Permen LHK No. 68/2016</b></li>
                <li><b>PP No. 22 Tahun 2021</b></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("Aplikasi ini sukses berjalan menggunakan Python dan Streamlit Framework.")
