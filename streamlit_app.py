import streamlit as st
import pandas as pd
from datetime import datetime, date
import requests
from streamlit_lottie import st_lottie

# 1. PENGATURAN HALAMAN
st.set_page_config(
    page_title="B3 Waste Tracker Pro",
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

# Memuat animasi Lottie yang berbeda untuk tiap halaman
lottie_home = load_lottieurl("https://lottie.host/549c44db-e204-4bda-be9f-86f37efbe065/wP8pMWeE6A.json") # Animasi Ekologi/Pabrik
lottie_form = load_lottieurl("https://lottie.host/409d6f6a-ce07-4286-9a25-9b24765ff0f5/H6q8S0vXzH.json") # Animasi Input/Data
lottie_about = load_lottieurl("https://lottie.host/51e3db3d-ef04-45fb-bc76-efdbb0cae5eb/tqNUnVjY02.json") # Animasi Sertifikat/Regulasi

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

# 5. HEADER UTAMA APLIKASI
st.title("☣️ Industrial Hazardous Waste Tracker")
st.markdown("---")

# 6. PEMBUATAN MENU NAVIGASI (3 TABS)
tab1, tab2, tab3 = st.tabs(["🏠 Beranda", "📥 Input & Hasil Data", "ℹ️ Tentang Aplikasi & Regulasi"])

# ==================== MENU 1: BERANDA ====================
with tab1:
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.header("Selamat Datang di Sistem Pemantauan Limbah B3")
        st.markdown("""
        ### Kenapa Aplikasi Ini Dibuat?
        Pengelolaan Limbah Bahan Berbahaya dan Beracun (B3) merupakan salah satu aspek paling krusial sekaligus sensitif dalam operasional industri modern. Kegagalan dalam melacak masa simpan limbah dapat memicu **sanksi hukum, denda finansial, hingga pencemaran lingkungan serius**.
        
        Aplikasi ini dikembangkan sebagai solusi digital berbasis data untuk:
        *   **Mencegah Pelanggaran Hukum:** Memberikan sistem peringatan dini sebelum masa simpan legal limbah di Tempat Penyimpanan Sementara (TPS) berakhir.
        *   **Standardisasi Pengemasan:** Menyediakan rekomendasi wadah penyimpanan yang tepat secara otomatis demi keselamatan kerja.
        *   **Transparansi Audit:** Mempermudah pencatatan logbook yang rapi, terstruktur, dan siap pakai untuk keperluan audit lingkungan internal maupun eksternal.
        """)
    with col_h2:
        if lottie_home:
            st_lottie(lottie_home, height=250, key="home_anim")

# ==================== MENU 2: INPUT & HASIL DATA ====================
with tab2:
    st.header("📝 Manajemen Inventaris TPS Limbah B3")
    
    col_f1, col_f2 = st.columns([1, 2])
    
    # Kiri: Form Input
    with col_f1:
        st.subheader("Form Input Limbah")
        if lottie_form:
            st_lottie(lottie_form, height=120, key="form_anim")
            
        with st.form(key="form_b3", clear_on_submit=True):
            jenis_limbah = st.selectbox("Pilih Jenis Limbah B3", list(B3_DATABASE.keys()))
            
            # Tampilan Otomatis Rekomendasi Wadah dan Simbol
            simbol_oto = B3_DATABASE[jenis_limbah]["simbol"]
            wadah_oto = B3_DATABASE[jenis_limbah]["wadah_rekomendasi"]
            
            st.caption(f"**Karakteristik:** {simbol_oto}")
            st.caption(f"**Rekomendasi Wadah:** {wadah_oto}")
            
            berat = st.number_input("Berat Limbah (Kg)", min_value=1.0, step=10.0)
            tgl_masuk = st.date_input("Tanggal Masuk TPS", date.today())
            
            submit_btn = st.form_submit_button(label="Simpan ke Sistem")
            
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
            st.success("Data Berhasil Disimpan!")

    # Kanan: Hasil Tabel & Tombol Download
    with col_f2:
        st.subheader("Tabel Pantauan Real-Time TPS")
        
        if st.session_state.b3_db.empty:
            st.info("Belum ada data masuk. Silakan isi form di sebelah kiri.")
        else:
            # Fungsi Mewarnai Baris Tabel
            def color_status(val):
                if "KRITIS" in str(val):
                    return "background-color: #ffcccc; color: black; font-weight: bold;"
                elif "Peringatan" in str(val):
                    return "background-color: #fff2cc; color: black;"
                return "background-color: #e2f0d9; color: black;"

            df_styled = st.session_state.b3_db.style.applymap(color_status, subset=["Status"])
            st.dataframe(df_styled, use_container_width=True)
            
            # FITUR DOWNLOAD DATA
            st.markdown("### 📥 Ekspor Laporan Logbook")
            
            # Konversi dataframe ke CSV
            csv_data = st.session_state.b3_db.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Unduh Data Logbook (Format .CSV)",
                data=csv_data,
                file_name=f"Logbook_Limbah_B3_{date.today()}.csv",
                mime="text/csv",
                help="Klik di sini untuk mengunduh laporan tabel di atas untuk kebutuhan Microsoft Excel atau laporan audit."
            )
            
            if st.button("Kosongkan Semua Data"):
                st.session_state.b3_db = pd.DataFrame(columns=[
                    "ID Limbah", "Jenis Limbah", "Karakteristik / Simbol", 
                    "Rekomendasi Wadah", "Berat (Kg)", "Tanggal Masuk", "Batas Hari", "Sisa Hari", "Status"
                ])
                st.rerun()

# ==================== MENU 3: TENTANG & REGULASI ====================
with tab3:
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
