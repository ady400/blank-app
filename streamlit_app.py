import time
import numpy as np
import pandas as pd
import streamlit as st
import io
from streamlit_lottie import st_lottie

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
            organik_input = st.number_input("Sampah Organik", min_value=0.0, step=0.1, value=0.0)
            anorganik_input = st.number_input("Sampah Anorganik", min_value=0.0, step=0.1, value=0.0)
            b3_input = st.number_input("Sampah B3 (Bahan Berbahaya & Beracun)", min_value=0.0, step=0.1, value=0.0)
            submitted = st.form_submit_button("Hitung dari Input")

        if submitted:
            total_manual = round(organik_input + anorganik_input + b3_input, 2)
            st.markdown("## 🔍 Hasil Input Manual")

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

            st.markdown("### Tips dari Sampahmu")
            if organik_input > anorganik_input:
                st.success("Kamu bisa mulai membuat kompos dari sampah organik.")
            if anorganik_input > 1:
                st.info("Kurangi plastik, gunakan ulang barang jika bisa.")
            if b3_input > 0.1:
                st.warning("Pisahkan limbah B3 seperti baterai atau elektronik kecil!")
