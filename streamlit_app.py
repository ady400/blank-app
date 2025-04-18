import streamlit as st

# Set Page Configuration
st.set_page_config(page_title="Aplikasi Edukasi Limbah Industri", layout="centered")

# Sidebar Navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Proses Pengolahan", "Kalkulator COD", "Kuis"])

# Halaman: Beranda
if menu == "Beranda":
    st.markdown("""
        <div style='text-align:center; padding: 30px 0;'>
            <h1 style='color: green;'>🌿 Selamat Datang di Aplikasi Edukasi Limbah Industri</h1>
            <p style='font-size:18px;'>Belajar pengolahan limbah industri jadi lebih mudah dan menyenangkan.</p>
        </div>
    """, unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/1146/1146855.png", width=150)

    st.success("✅ Aplikasi ini dirancang untuk mahasiswa Teknik Lingkungan dan sejenisnya.")

    st.markdown("### 📌 Tips Menggunakan Aplikasi Ini:")
    st.markdown("""
    - Navigasikan materi melalui sidebar ⬅️
    - Gunakan Kalkulator COD untuk bantu hitung parameter laboratorium
    - Ikuti kuis untuk menguji pemahamanmu
    """)

    st.markdown("---")
    st.markdown("<center>© 2025 EduWaste | Dibuat dengan Streamlit</center>", unsafe_allow_html=True)

# Halaman: Proses Pengolahan
elif menu == "Proses Pengolahan":
    st.title("🔬 Proses Pengolahan Limbah Cair Industri")

    st.markdown("""
    Limbah cair industri harus diolah sebelum dibuang ke lingkungan. Proses ini terdiri dari beberapa tahap:

    ### 1. *Screening*
    Memisahkan benda padat kasar seperti plastik, kayu, dll.

    ### 2. *Equalization*
    Menyeimbangkan debit dan konsentrasi limbah agar lebih stabil.

    ### 3. *Koagulasi-Flokulasi*
    Menghilangkan partikel tersuspensi dengan penambahan bahan kimia.

    ### 4. *Aerasi*
    Mengaktifkan mikroorganisme untuk mengurai zat organik.

    ### 5. *Sedimentasi*
    Mengendapkan partikel yang telah menggumpal.

    ### 6. *Desinfeksi*
    Membunuh mikroorganisme patogen sebelum dibuang ke badan air.
    """)

    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050440.png", width=150)

# Halaman: Kalkulator COD
elif menu == "Kalkulator COD":
    st.title("🧪 Kalkulator COD")

    st.markdown("Masukkan nilai-nilai berikut untuk menghitung Chemical Oxygen Demand (COD):")

    V_blank = st.number_input("Volume titrasi blanko (mL)", min_value=0.0)
    V_sample = st.number_input("Volume titrasi sampel (mL)", min_value=0.0)
    N = st.number_input("Normalitas larutan titran (N)", min_value=0.0)
    Volume_sample = st.number_input("Volume sampel (mL)", min_value=0.0)

    if st.button("Hitung COD"):
        try:
            cod = ((V_blank - V_sample) * N * 8000) / Volume_sample
            st.success(f"Nilai COD: {cod:.2f} mg/L")
        except ZeroDivisionError:
            st.error("Volume sampel tidak boleh nol.")

# Halaman: Kuis Edukasi
elif menu == "Kuis":
    st.title("📝 Kuis Edukasi Pengolahan Limbah")

    st.markdown("Jawab pertanyaan berikut untuk menguji pemahamanmu:")

    q1 = st.radio("1. Apa tujuan proses aerasi dalam pengolahan limbah?", 
                ["Memisahkan padatan", "Menghilangkan logam berat", "Mengurai zat organik", "Membunuh mikroba"])

    q2 = st.radio("2. COD adalah parameter yang mengukur ...", 
                ["Jumlah mikroba", "Kekeruhan air", "Kebutuhan oksigen kimia", "pH air"])

    if st.button("Lihat Hasil"):
        score = 0
        if q1 == "Mengurai zat organik":
            score += 1
        if q2 == "Kebutuhan oksigen kimia":
            score += 1
        st.success(f"Skor kamu: {score}/2")
