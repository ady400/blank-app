import streamlit as st

# ==========================================
# CONFIGURATION & THEME (Nuansa Hijau)
# ==========================================
st.set_page_config(
    page_title="EcoWater COD Analyzer",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk mempercantik UI dengan sentuhan warna hijau
st.markdown("""
    <style>
    /* Mengubah warna font utama & background sidebar secara subtle */
    .stApp {
        background-color: #f9fbf9;
    }
    h1, h2, h3 {
        color: #2e6f40 !important;
    }
    /* Style untuk kartu/box informasi */
    .custom-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2e6f40;
        margin-bottom: 20px;
    }
    .success-card {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #c8e6c9;
        color: #2e7d32;
    }
    .danger-card {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffcdd2;
        color: #c62828;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/illustrations/external-pack-avocado-flaticons-lineal-color-flat-icons/100/external-ecology-green-energy-pack-avocado-flaticons-lineal-color-flat-icons.png", width=100)
    st.title("EcoWater Nav")
    st.markdown("---")
    menu = st.radio(
        "Pilih Halaman:",
        ["🏠 Home", "🧮 Kalkulator COD", "ℹ️ Tentang Aplikasi"],
        index=0
    )
    st.markdown("---")
    st.caption("EcoWater Analyzer v1.0 © 2026")

# ==========================================
# HALAMAN 1: HOME
# ==========================================
if menu == "🏠 Home":
    st.title("🌱 EcoWater COD Analyzer")
    st.subheader("Solusi Digital Pemantauan Kualitas Air Limbah")
    
    st.image("https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?auto=format&fit=crop&w=800&q=80", caption="Komitmen menjaga kelestarian lingkungan melalui monitoring air limbah.", use_container_width=True)
    
    st.markdown("""
    ### 📌 Tentang Web Ini
    **EcoWater COD Analyzer** adalah platform berbasis web yang dirancang untuk mempermudah praktisi lingkungan, 
    laboran, maupun mahasiswa dalam melakukan kalkulasi dan analisis kadar **Chemical Oxygen Demand (COD)** pada air limbah.
    
    ### 🚀 Fitur Utama:
    * **Kalkulasi Akurat:** Menghitung kadar COD berdasarkan volume titran secara instan.
    * **Evaluasi Baku Mutu:** Otomatis membandingkan hasil uji dengan regulasi lingkungan hidup yang berlaku.
    * **Umpan Balik Visual:** Indikator warna hijau (Lolos) atau merah (Melebihi Batas) untuk mempermudah pengambilan keputusan (Asesmen Cepat).
    """)

# ==========================================
# HALAMAN 2: KALKULATOR COD
# ==========================================
elif menu == "🧮 Kalkulator COD":
    st.title("🧮 Kalkulator Kadar COD")
    st.write("Masukkan parameter hasil titrasi laboratorium Anda untuk menghitung nilai COD.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📥 Input Data Titrasi")
        # Input parameter rumus COD umum: (A - B) * N * 8000 / V_sampel
        v_blanko = st.number_input("Volume Penitar Blanko (mL)", min_value=0.0, value=10.0, step=0.1)
        v_sampel_titrasi = st.number_input("Volume Penitar Sampel (mL)", min_value=0.0, value=6.5, step=0.1)
        normalitas = st.number_input("Normalitas Larutan Penitar (N)", min_value=0.000, value=0.100, format="%.4f", step=0.001)
        v_air_sampel = st.number_input("Volume Sampel Air (mL)", min_value=1.0, value=25.0, step=1.0)
        
    with col2:
        st.markdown("### 📋 Standar Regulasi")
        # Pilihan Baku Mutu (Bisa disesuaikan dengan Permen LHK)
        baku_mutu_opsi = {
            "Limbah Domestik (Permen LHK No. 68/2016)": 100.0,
            "Limbah Industri Kimia Umum": 250.0,
            "Air Sungai Kelas II (PP No. 22/2021)": 25.0,
            "Custom (Input Manual)": 0.0
        }
        
        pilihan = st.selectbox("Pilih Acuan Baku Mutu:", list(baku_mutu_opsi.keys()))
        
        if pilihan == "Custom (Input Manual)":
            baku_mutu = st.number_input("Masukkan Batas Maksimal COD (mg/L)", min_value=0.0, value=50.0)
        else:
            baku_mutu = baku_mutu_opsi[pilihan]
            st.info(f"Batas Maksimal COD untuk standar ini: **{baku_mutu} mg/L**")

    # Tombol Hitung
    st.markdown("---")
    if st.button("🚀 Hitung & Analisis Status", use_container_width=True):
        
        # Rumus Kimia COD: ((V_blanko - V_sampel) * N * 8000) / V_air_sampel
        # Penjagaan agar tidak minus jika input keliru
        if v_blanko < v_sampel_titrasi:
            st.error("⚠️ Kesalahan: Volume blanko harus lebih besar atau sama dengan volume sampel!")
        else:
            hasil_cod = ((v_blanko - v_sampel_titrasi) * normalitas * 8000) / v_air_sampel
            
            # Tampilkan Hasil Utama
            st.markdown("### 📊 Hasil Analisis")
            
            # Menggunakan st.metric untuk visual yang elegan
            st.metric(label="Nilai COD Terhitung", value=f"{hasil_cod:.2f} mg/L")
            
            # Evaluasi kelulusan baku mutu
            if hasil_cod <= baku_mutu:
                st.markdown(f"""
                <div class="success-card">
                    <h4>🟢 STATUS: LOLOS BAKU MUTU</h4>
                    <p>Kadar COD sebesar <b>{hasil_cod:.2f} mg/L</b> berada di bawah atau sama dengan batas aman yang ditetapkan (<b>{baku_mutu:.1f} mg/L</b>).</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f"""
                <div class="danger-card">
                    <h4>🔴 STATUS: MELEBIHI BAKU MUTU (TIDAK LOLOS)</h4>
                    <p>Kadar COD sebesar <b>{hasil_cod:.2f} mg/L</b> telah melewati batas maksimal yang diperbolehkan (<b>{baku_mutu:.1f} mg/L</b>). Diperlukan pengolahan air limbah (IPAL) lebih lanjut sebelum dibuang ke lingkungan.</p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: TENTANG APLIKASI
# ==========================================
elif menu == "ℹ️ Tentang Aplikasi":
    st.title("ℹ️ Informasi Aplikasi & Referensi")
    
    # Box Pembuat
    st.markdown("""
    <div class="custom-card">
        <h3>👤 Profil Pembuat</h3>
        <p>Aplikasi ini dikembangkan sebagai alat bantu presentasi interaktif untuk simulasi kelayakan buangan parameter COD pada unit pengolahan limbah.</p>
        <ul>
            <li><b>Nama Pengembang:</b> Raehan Ady Saesya & Tim</li>
            <li><b>Fokus Bidang:</b> Environmental Engineering / Industrial Chemistry</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Box Referensi
    st.markdown("""
    <div class="custom-card">
        <h3>📚 Referensi & Dasar Hukum</h3>
        <p>Perhitungan dan standar baku mutu pada aplikasi ini mengacu pada dokumen resmi berikut:</p>
        <ol>
            <li><b>SNI 6989.2:2019</b> - Air dan air limbah – Bagian 2: Cara uji Kebutuhan Oksigen Kimiawi (Chemical Oxygen Demand/COD) dengan refluks tertutup secara spektrofotometri/titrasi.</li>
            <li><b>Peraturan Menteri Lingkungan Hidup dan Kehutanan RI No. P.68/Menlhk-Setjen/2016</b> tentang Baku Mutu Air Limbah Domestik.</li>
            <li><b>Peraturan Pemerintah (PP) No. 22 Tahun 2021</b> tentang Penyelenggaraan Perlindungan dan Pengelolaan Lingkungan Hidup (Lampiran VI - Baku Mutu Air Nasional).</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
