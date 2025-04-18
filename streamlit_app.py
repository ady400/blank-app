mport streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="WasteVisual", layout="centered")

st.title("WasteVisual: Visualisasi Data Limbah Industri")

# Upload file CSV
uploaded_file = st.file_uploader("Unggah file CSV berisi data limbah", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Limbah yang Diupload:")
    st.dataframe(df)

    # Visualisasi COD
    st.subheader("Grafik COD")
    fig_cod = px.line(df, x='Tanggal', y='COD (mg/L)', markers=True, title="Tren COD")
    st.plotly_chart(fig_cod)

    # Visualisasi BOD
    st.subheader("Grafik BOD")
    fig_bod = px.line(df, x='Tanggal', y='BOD (mg/L)', markers=True, title="Tren BOD")
    st.plotly_chart(fig_bod)

    # Analisis ambang batas (misal COD > 200, BOD > 80)
    st.subheader("Analisis Kepatuhan Ambang Batas")
    cod_batas = 200
    bod_batas = 80

    cod_melebihi = df[df['COD (mg/L)'] > cod_batas]
    bod_melebihi = df[df['BOD (mg/L)'] > bod_batas]

    st.markdown(f"*Jumlah hari COD melebihi batas ({cod_batas} mg/L):* {len(cod_melebihi)}")
    st.markdown(f"*Jumlah hari BOD melebihi batas ({bod_batas} mg/L):* {len(bod_melebihi)}")

    if not cod_melebihi.empty:
        st.warning("Hari-hari dengan COD melebihi batas:")
        st.dataframe(cod_melebihi[['Tanggal', 'COD (mg/L)']])

    if not bod_melebihi.empty:
        st.warning("Hari-hari dengan BOD melebihi batas:")
        st.dataframe(bod_melebihi[['Tanggal', 'BOD (mg/L)']])
else:
    st.info("Silakan unggah file CSV terlebih dahulu.")
