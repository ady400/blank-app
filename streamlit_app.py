import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests
from streamlit_lottie import st_lottie

# 1. PENGATURAN HALAMAN
st.set_page_config(
    page_title="Storify Waste",
    page_icon="☣️",
    layout="wide"
)

# 2. FUNGSI MEMUAT ANIMASI LOTTIE
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

# Memuat animasi Lottie
lottie_home = load_lottieurl("https://lottie.host/947d937e-1b76-43a0-b786-d255c0ee1e74/stE5uwmVhW.json") 
lottie_form = load_lottieurl("https://lottie.host/409d6f6a-ce07-4286-9a25-9b24765ff0f5/H6q8S0vXzH.json") # Input/Data
lottie_about = load_lottieurl("https://lottie.host/51e3db3d-ef04-45fb-bc76-efdbb0cae5eb/tqNUnVjY02.json") # Sertifikat/Regulasi

# 3. DATABASE DAN REKOMENDASI WADAH OTOMATIS
B3_DATABASE = {
    "Sludge IPAL / Elektroplating": {
        "simbol": "☣️ Beracun (Toxic)", 
        "masa_simpan": 90,
        "wadah_rekomendasi": "Drum Plastik (HDPE Drum) atau Jumbo Bag dengan pelapis dalam (inner liner) untuk mencegah kebocoran material basah."
    },
    "Oli Bekas / Solvent": {
        "simbol": "🔥 Mudah Menyala (Flammable)", 
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) yang dilengkapi dengan seal penutup rapat untuk menahan tekanan uap cair."
    },
    "Aki Bekas / Asam-Asaman": {
        "simbol": "🧪 Korosif (Corrosive)", 
        "masa_simpan": 365,
        "wadah_rekomendasi": "Box Container Plastic / Palet Plastik HDPE khusus yang tahan terhadap korosi asam dan zat kimia tajam."
    },
    "Kain Majun Terkontaminasi": {
        "simbol": "⚠️ Bahaya Terhadap Kesehatan", 
        "masa_simpan": 180,
        "wadah_rekomendasi": "Drum Baja (Steel Drum) atau Container Tertutup untuk meminimalisir risiko penyebaran kontaminan ke udara."
    },
    "Fly Ash / Bottom Ash": {
        "simbol": "☣️ Beracun (Toxic)", 
        "masa_simpan": 365,
        "wadah_rekomendasi": "Jumbo Bag tipe tertutup rapat (Woven PP dengan liner) untuk menghindari emisi debu halus ke lingkungan sekitar."
    }
}

# 4. INITIALIZATION SESSION STATE (Simulasi Database)
if "b3_db" not in st.session_state:
    st.session_state.b3_db = pd.DataFrame(columns=[
        "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
        "Rekomendasi Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
    ])

# ==================== SIDEBAR (NAVIGASI SAMPING) ====================
with st.sidebar:
    st.title("☣️ Storify Waste")
    st.markdown("Sistem Kepatuhan TPS")
    st.markdown("---")
    
    # Komponen Radio Button untuk Navigasi Samping
    menu_pilihan = st.radio(
        "Pilih Menu Navigasi:",
        ["🏠 Beranda Utama", "📥 Input & Hasil Data", "ℹ️ Tentang & Regulasi"]
    )
    
    st.markdown("---")
    st.caption("Aplikasi Pemantauan Digital v1.1")

# ==================== LOGIKA HALAMAN UTAMA ====================

# 📑 MENU 1: BERANDA UTAMA
if menu_pilihan == "🏠 Beranda Utama":
    
    # 1. Tampilkan animasi Lottie di bagian paling atas
    if lottie_home:
        st_lottie(lottie_home, speed=1, loop=True, quality="high", height=200)
    
    st.markdown("<br>", unsafe_allow_html=True) # Memberi sedikit jarak vertikal
    
    # 2. Judul dengan Background CSS kustom
    st.markdown(
        """
        <div style="
            background-color: #1e4620; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 25px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        ">
            <h1 style="color: white; margin: 0; font-size: 28px; text-align: center;">
                🌿 Selamat Datang di Sistem Pemantauan Limbah B3
            </h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 3. Tampilkan teks penjelasan di bawahnya
    st.markdown("""
    ### Kenapa Aplikasi Ini Dibuat?
    Pengelolaan Limbah Bahan Berbahaya dan Beracun (B3) merupakan salah satu aspek paling krusial sekaligus sensitif dalam operasional industri modern.
    
    Aplikasi ini dikembangkan sebagai solusi digital berbasis data untuk:
    * **Mencegah Pelanggaran Hukum:** Memberikan sistem peringatan dini sebelum masa simpan legal limbah di Tempat Penyimpanan Sementara (TPS) berakhir.
    * **Standardisasi Pengemasan:** Menyediakan rekomendasi wadah penyimpanan yang tepat secara otomatis demi keselamatan kerja.
    * **Transparansi Audit:** Mempermudah pencatatan logbook yang rapi, terstruktur, dan siap pakai untuk keperluan audit lingkungan internal maupun eksternal.
    """)
    
# 📑 MENU 2: INPUT & HASIL DATA
elif menu_pilihan == "📥 Input & Hasil Data":
    
    # 1. Tampilkan animasi Lottie di bagian paling atas halaman menu 2
    if lottie_form:
        st_lottie(lottie_form, speed=1, loop=True, quality="high", height=180, key="form_menu_top")
    
    st.markdown("<br>", unsafe_allow_html=True) # Jarak vertikal halus
    
    # 2. Judul Halaman dengan Background Kustom yang Menarik
    st.markdown(
        """
        <div style="
            background-color: #2c3e50; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
        ">
            <h2 style="color: white; margin: 0; font-size: 26px; text-align: center; font-family: 'Source Sans Pro', sans-serif;">
                📥 Manajemen Inventaris & Logbook Digital TPS B3
            </h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 3. Pembagian Kolom untuk Form dan Tabel di bawah Judul Utama
    col_f1, col_f2 = st.columns([1, 2])
    
    # Sisi Kiri: Form Input
    with col_f1:
        st.subheader("📝 Entri Limbah Masuk")
            
        with st.form(key="form_b3", clear_on_submit=True):
            jenis_limbah = st.selectbox("Pilih Jenis Limbah B3", list(B3_DATABASE.keys()))
            
            simbol_oto = B3_DATABASE[jenis_limbah]["simbol"]
            wadah_oto = B3_DATABASE[jenis_limbah]["wadah_rekomendasi"]
            
            # Info box otomatis yang rapi di dalam form
            st.info(f"**Karakteristik:** {simbol_oto}\n\n**Rekomendasi Wadah:** {wadah_oto}")
            
            berat = st.number_input("Berat Limbah (Kg)", min_value=1.0, step=10.0)
            tgl_masuk = st.date_input("Tanggal Masuk TPS", date.today())
            
            submit_btn = st.form_submit_button(label="Simpan ke Logbook")
            
        if submit_btn:
            id_limbah = f"B3-{datetime.now().strftime('%M%S')}"
            batas_hari = B3_DATABASE[jenis_limbah]["masa_simpan"]
            sisa_hari = batas_hari - (date.today() - tgl_masuk).days
            
            status = "Aman"
            if sisa_hari <= 14:
                status = "KRITIS 🔴"
            elif sisa_hari <= 30:
                status = "Peringatan 🟡"

            new_data = pd.DataFrame([{
                "ID Limbah": id_limbah,
                "Jenis Limbah": jenis_limbah,
                "Karakteristik / Simbol": simbol_oto,
                "Rekomendasi Wadah": wadah_oto,
                "Berat (Kg)": berat,
                "Tanggal Masuk": tgl_masuk,
                "Batas Hari": f"{batas_hari} Hari",
                "Sisa Hari": sisa_hari,
                "Status": status
            }])
            
            st.session_state.b3_db = pd.concat([st.session_state.b3_db, new_data], ignore_index=True)
            st.success("Data Berhasil Disimpan ke TPS!")
            st.rerun()

    # Sisi Kanan: Hasil Tabel & Tombol Download
    with col_f2:
        st.subheader("📊 Tabel Pantauan Real-Time TPS")
        
        if st.session_state.b3_db.empty:
            st.info("Belum ada data masuk. Silakan isi form entri di sebelah kiri.")
        else:
            # Fungsi pewarnaan status tabel
            def color_status(val):
                if "KRITIS" in str(val):
                    return "background-color: #ffcccc; color: black; font-weight: bold;"
                elif "Peringatan" in str(val):
                    return "background-color: #fff2cc; color: black;"
                return "background-color: #e2f0d9; color: black;"

            df_styled = st.session_state.b3_db.style.applymap(color_status, subset=["Status"])
            st.dataframe(df_styled, use_container_width=True)
            
            # FITUR DOWNLOAD DATA
            st.markdown("---")
            st.markdown("### 📥 Ekspor Laporan Resmi")
            csv_data = st.session_state.b3_db.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Unduh Data Logbook (.CSV)",
                data=csv_data,
                file_name=f"Logbook_Limbah_B3_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Kosongkan Semua Data TPS", use_container_width=True):
                st.session_state.b3_db = pd.DataFrame(columns=[
                    "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
                    "Rekomendasi Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
                ])
                st.rerun()

# 📑 MENU 3: TENTANG & REGULASI
elif menu_pilihan == "ℹ️ Tentang & Regulasi":
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        st.header("Informasi Pengembang & Acuan Baku Mutu")
        st.markdown("""
        ### 📚 Regulasi / Acuan Baku Mutu Utama
        Sistem penentuan karakteristik piktogram bahaya, tata cara pengemasan, dan batasan masa penyimpanan di dalam aplikasi ini dikembangkan dengan mengacu ketat pada hukum positif di Indonesia:
        1.  **Peraturan Pemerintah (PP) No. 22 Tahun 2021** tentang *Penyelenggaraan Perlindungan dan Pengelolaan Lingkungan Hidup* (Lampiran IX mengenai Pengelolaan Limbah B3).
        2.  **Peraturan Menteri LHK No. 6 Tahun 2021** tentang *Tata Cara dan Persyaratan Pengelolaan Limbah Bahan Berbahaya dan Beracun*.
        3.  **Sistem Harmonisasi Global (GHS - Globally Harmonized System)** untuk standardisasi simbol piktogram bahaya zat kimia.

        ### 💻 Profil Pengembang
        Aplikasi purwarupa (*prototype*) ini dirancang dan dibangun oleh pengembang yang berfokus pada integrasi **Teknologi Informasi** di bidang **Teknik Lingkungan & Keselamatan Kerja (K3)**. 
        
        *   **Tujuan Proyek:** Menyediakan alat bantu digital yang intuitif bagi operator lapangan dan manajemen industri dalam memitigasi risiko hukum dan operasional terkait limbah beracun.
        """)
    with col_a2:
        if lottie_about:
            st_lottie(lottie_about, height=250, key="about_anim")
