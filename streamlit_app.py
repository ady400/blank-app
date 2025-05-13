import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# ------ SETTING HALAMAN ------
st.set_page_config(page_title="🧮Kalkulator Sampah", layout="wide")

# ------ FUNGSI LOTTIE ------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ------ LOAD LOTTIE ANIMASI ------
lottie_beranda = load_lottieurl("https://lottie.host/7012c055-a4d1-45ed-a418-072d297976da/oNk7iDlYc4.json")
lottie_kalkulator = load_lottieurl("https://lottie.host/111b6b6e-bf2c-4038-ac15-befa1b812447/hcB9Tj71nP.json")
lottie_proses = load_lottieurl("https://lottie.host/86f268c8-56cf-48dd-9386-dbbaec9c85a3/6nnch2E4UO.json")
lottie_tentang = load_lottieurl("https://lottie.host/be996198-0326-4825-84ab-df2b87cf6fe7/abSuY84DLW.json")
lottie_sidebar = load_lottieurl("https://lottie.host/ecf5efac-13f3-4b3f-8f18-db129ef7022b/9UjhCTdYbi.json")


# ------ MENU NAVIGASI ------
with st.sidebar:
    st_lottie(lottie_sidebar, speed=1, loop=True, quality="high", height=150)
    st.title("♻️ kalkulator Sampah Harian")
    st.markdown("Belajar Pengolahan Sampah harian")
    st.markdown("---")
    menu = st.radio("Navigasi", ["🏠 Beranda", "🔄 Proses", "🧮 Kalkulator", "ℹ️ Tentang"])
    st.markdown("---")

# ------ STYLE TAMBAHAN ------
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f4f3;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .bottom-nav {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f4f3;
        padding: 10px 0;
        text-align: center;
        font-size: 16px;
        color: #2E7D32;
        border-top: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# ------ BERANDA ------
if menu == "🏠 Beranda":
    st_lottie(lottie_beranda, speed=1, loop=True, quality="high", height=300)
    st.markdown("<div style='margin-top: 30px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1 style='color:#2C3E50;'>♻️ Kalkulator sampah harian ♻️</h1>
        <p style='font-size:18px; color:#555;'>Belajar tahapan umum pengolahan sampah harian.</p>
    </div>
    """, unsafe_allow_html=True)
# ------ PROSES ------
elif menu == "🔄 Proses":
    st_lottie(lottie_proses, speed=1, loop=True, quality="high", height=200)
    st.markdown("<div style='margin-top: 30px'></div>", unsafe_allow_html=True)
    st.title("🔄 Proses Pengelolaan Sampah")

    st.markdown("Berikut adalah tahapan umum dalam pengelolaan sampah rumah tangga:")

    with st.expander("📌 1. Pemilahan"):
        st.write("Pisahkan sampah menjadi Organik, Anorganik, dan B3 sejak di rumah.")
        

    with st.expander("📌 2. Pengumpulan"):
        st.write("Sampah dikumpulkan berdasarkan jenis untuk memudahkan pemrosesan.")
       

    with st.expander("📌 3. Pengangkutan"):
        st.write("Petugas kebersihan mengangkut sampah ke TPS atau pusat daur ulang.")
        

    with st.expander("📌 4. Pemrosesan / Daur Ulang"):
        st.write("Organik → Kompos, Anorganik → Daur ulang, B3 → Penanganan khusus.")
        

    with st.expander("📌 5. Pembuangan Akhir"):
        st.write("Sampah sisa yang tidak bisa diproses dibuang ke TPA secara aman.")
        


# ------ KALKULATOR ------
elif menu == "🧮 Kalkulator":
    st_lottie(lottie_kalkulator, speed=1, loop=True, quality="high", height=200)
    st.markdown("<div style='margin-top: 30px'></div>", unsafe_allow_html=True)
    st.title("🧮 Hitung Sampah Harianmu")
    st.write("Pilih metode perhitungan sampah harian:")

    mode = st.radio("Mode Kalkulasi", ["Otomatis", "Input Manual"])

    if mode == "Otomatis":
        st.subheader("📊 Estimasi Berdasarkan Aktivitas")
        people = st.slider("Jumlah orang di rumah", 1, 10, 3)
        activity = st.radio("Tingkat aktivitas harian", ["Normal", "Aktif", "Banyak belanja"])

        base_waste = 0.7
        if activity == "Aktif":
            base_waste += 0.2
        elif activity == "Banyak belanja":
            base_waste += 0.5

        total = round(people * base_waste, 2)
        organik = total * 0.6
        anorganik = total * 0.35
        b3 = total * 0.05

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Sampah", f"{total} kg")
        with col2:
            st.metric("Sampah per Orang", f"{base_waste:.2f} kg")

        fig = px.pie(
            names=["Organik", "Anorganik", "B3"],
            values=[organik, anorganik, b3],
            color_discrete_sequence=['#81C784', '#4FC3F7', '#FF8A65'],
            title="Komposisi Sampah (Estimasi)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Tips")
        if organik > anorganik:
            st.success("Mulai kompos dari sekarang!")
        if anorganik > 1:
            st.info("Kurangi plastik dan belanja bijak.")
        if b3 > 0.1:
            st.warning("Pisahkan limbah B3 seperti baterai!")

    else:
        st.subheader("✍️ Input Manual Sampah")
        people = st.slider("Jumlah orang di rumah", 1, 10, 3)
           with st.form("sampah_input_form"):
            organik_input = st.number_input("Sampah Organik (kg)", min_value=0.0, step=0.1, value=0.0)
            anorganik_input = st.number_input("Sampah Anorganik (kg)", min_value=0.0, step=0.1, value=0.0)
            b3_input = st.number_input("Sampah B3 (kg)", min_value=0.0, step=0.1, value=0.0)
            submitted = st.form_submit_button("Hitung dari Input")

if submitted:
    total_manual = round(organik_input + anorganik_input + b3_input, 2)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Sampah", f"{total_manual} kg")
    with col2:
        st.metric("Sampah per Orang", f"{total_manual / people:.2f} kg")

    fig_manual = px.pie(
        names=["Organik", "Anorganik", "B3"],
        values=[organik_input, anorganik_input, b3_input],
        color_discrete_sequence=['#AED581', '#4FC3F7', '#FF8A65'],
        title="Komposisi Sampah dari Input"
    )
    st.plotly_chart(fig_manual, use_container_width=True)

    # Tips aman diletakkan DI SINI
    if total_manual > 0:
        st.markdown("### Tips dari Sampahmu")
        if organik_input > anorganik_input:
            st.success("Kamu bisa mulai membuat kompos dari sampah organik.")
        if anorganik_input > 1:
            st.info("Kurangi plastik, gunakan ulang barang jika bisa.")
        if b3_input > 0.1:
            st.warning("Pisahkan limbah B3 seperti baterai atau elektronik kecil!")



# ------ TENTANG ------
elif menu == "ℹ️ Tentang":
    st_lottie(lottie_tentang, speed=1, loop=True, quality="high", height=150)
    st.markdown("<div style='margin-top: 30px'></div>", unsafe_allow_html=True)
    st.title("ℹ️ Tentang Aplikasi")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        Aplikasi ini dirancang untuk:
        - Mengedukasi tentang sampah harian rumah tangga  
        - Menyediakan tips pengurangan limbah  
        - Mendorong gaya hidup berkelanjutan  

        **Dibuat oleh:** Kelompok 5-PLI AKA
        
        **Teknologi:** Streamlit + Plotly + Lottie  
        """)
    
