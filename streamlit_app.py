import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="EcoEngineer Pro-Dash",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #2E7D32; text-align: center; margin-bottom: 2rem;}
    .metric-card {background-color: #E8F5E8; padding: 1rem; border-radius: 10px; border-left: 5px solid #4CAF50;}
    .status-pass {color: #4CAF50; font-weight: bold; font-size: 1.2rem;}
    .status-fail {color: #F44336; font-weight: bold; font-size: 1.2rem;}
</style>
""", unsafe_allow_html=True)

# Data Baku Mutu PP No. 22 Tahun 2021
BAKU_MUTU = {'BOD5': 30, 'COD': 100, 'TSS': 30, 'pH': (6, 9), 'NH3-N': 5}

def calculate_unit_sizing(Q, td, surface_loading_rate=24):
    V = Q * td / 24
    A = Q / surface_loading_rate
    H = 3.5
    L = math.sqrt(A * 3)
    W = math.sqrt(A / 3)
    return {'Volume': round(V, 2), 'Luas': round(A, 2), 'Panjang': round(L, 2), 'Lebar': round(W, 2), 'Tinggi': H}

def stoichiometry_coagulant(BOD_in, Q, coagulant_type='FeCl3'):
    ratios = {'FeCl3': 8, 'Alum': 10, 'PAC': 6}
    dosage = BOD_in * ratios.get(coagulant_type, 8) * Q / 1000
    return round(dosage, 2)

def calculate_efficiency(influent, effluent):
    return ((influent - effluent) / influent * 100) if influent > 0 else 0

def check_regulation(effluent):
    status = {}
    for param, limit in BAKU_MUTU.items():
        if param == 'pH':
            status[param] = effluent[param] >= limit[0] and effluent[param] <= limit[1]
        else:
            status[param] = effluent[param] <= limit
    return status

# Header
st.markdown('<h1 class="main-header">🌱 EcoEngineer Pro-Dash</h1>', unsafe_allow_html=True)
st.markdown("**Dashboard Desain & Monitoring Instalasi Pengolahan Limbah**")

# Sidebar navigasi
st.sidebar.title("📋 Menu")
page = st.sidebar.selectbox("Pilih Fitur:", [
    "🏗️ Unit Sizing", "🧪 Stoichiometry", "📊 Simulasi Real-time", "✅ Regulatory Checker"
])

# Halaman 1: Unit Sizing
if page == "🏗️ Unit Sizing":
    st.header("🏗️ Automatic Unit Sizing")
    col1, col2 = st.columns(2)
    
    with col1:
        Q = st.number_input("**Debit (Q)** (m³/hari)", min_value=1.0, value=100.0, step=10.0)
        td = st.number_input("**Waktu Tinggal (t_d)** (jam)", min_value=1.0, value=24.0, step=1.0)
        SLR = st.number_input("**Surface Loading Rate** (m³/m².hari)", min_value=5.0, value=24.0, step=1.0)
    
    with col2:
        if st.button("💾 Hitung Dimensi", type="primary"):
            dimensions = calculate_unit_sizing(Q, td, SLR)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("**Volume**", f"{dimensions['Volume']} m³")
            with col_b: st.metric("**Luas**", f"{dimensions['Luas']} m²")
            with col_c: st.metric("**P x L x T**", f"{dimensions['Panjang']}×{dimensions['Lebar']}×{dimensions['Tinggi']} m")
            
            # Fixed 3D plot
            fig = go.Figure(data=[go.Surface(z=[[dimensions['Tinggi'], dimensions['Tinggi']], 
                                           [dimensions['Tinggi'], dimensions['Tinggi']]],
                                  x=[[0, dimensions['Panjang']], [0, dimensions['Panjang']]],
                                  y=[[0, dimensions['Lebar']], [0, dimensions['Lebar']]],
                                  colorscale='Viridis', showscale=False)])
            fig.update_layout(title="3D Bak Preview", scene=dict(xaxis_title='Panjang', 
                                                                 yaxis_title='Lebar', 
                                                                 zaxis_title='Tinggi'))
            st.plotly_chart(fig, use_container_width=True)

# Halaman 2: Stoichiometry
elif page == "🧪 Stoichiometry":
    st.header("🧪 Stoichiometry Calculator")
    col1, col2 = st.columns(2)
    
    with col1:
        BOD_in = st.number_input("**BOD Masuk** (mg/L)", min_value=0.0, value=200.0)
        Q_stoich = st.number_input("**Debit** (m³/hari)", min_value=1.0, value=100.0)
        coagulant = st.selectbox("**Jenis Koagulan**", ['FeCl3', 'Alum', 'PAC'])
    
    with col2:
        dosage = stoichiometry_coagulant(BOD_in, Q_stoich, coagulant)
        st.metric("**Kebutuhan Koagulan**", f"{dosage} kg/hari")
        st.info(f"**Rasio**: 1 mg {coagulant} per {8 if coagulant=='FeCl3' else 10 if coagulant=='Alum' else 6} mg BOD")
    
    st.subheader("📋 Rekomendasi Jar Test")
    jar_data = {'Koagulan': ['FeCl3', 'Alum', 'PAC'], 'Dosis Optimal': ['200-800 mg/L', '300-1000 mg/L', '150-600 mg/L'], 'pH Optimal': ['6.5-7.5', '6.0-7.5', '6.5-8.0']}
    st.table(pd.DataFrame(jar_data))

# Halaman 3: Simulasi (FIXED - Tanpa Indicator di subplots)
elif page == "📊 Simulasi Real-time":
    st.header("📊 Interactive Simulation")
    
    col1, col2, col3 = st.columns(3)
    with col1: BOD_in_sim = st.slider("**BOD Masuk** (mg/L)", 50, 500, 200)
    with col2: Q_sim = st.slider("**Debit** (m³/hari)", 50, 500, 100)
    with col3: efficiency = st.slider("**Efisiensi (%)**", 50.0, 95.0, 85.0, 0.5)
    
    BOD_out_sim = BOD_in_sim * (1 - efficiency/100)
    
    # FIXED: 2x2 subplots TANPA Indicator
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Efisiensi Penyisihan', 'Konsentrasi BOD', 'Volume vs Debit', 'Status BOD'))
    
    # Plot 1: Efisiensi curve
    fig.add_trace(go.Scatter(x=[50,100,200,300,400,500], y=[95,90,85,80,75,70], mode='lines+markers', name='Target'), row=1, col=1)
    
    # Plot 2: BOD Bar
    fig.add_trace(go.Bar(x=['Masuk', 'Keluar'], y=[BOD_in_sim, BOD_out_sim], marker_color=['#FF6384', '#36A2EB'], name='BOD'), row=1, col=2)
    
    # Plot 3: Volume vs Debit
    debits = np.linspace(50, 500, 10)
    volumes = [calculate_unit_sizing(q, 24)['Volume'] for q in debits]
    fig.add_trace(go.Scatter(x=debits, y=volumes, mode='lines', name='Volume Bak'), row=2, col=1)
    
    # Plot 4: BOD Gauge (Bar instead of Indicator)
    bod_status = '✅ Lulus' if BOD_out_sim <= BAKU_MUTU['BOD5'] else '❌ Gagal'
    colors = ['green' if BOD_out_sim <= BAKU_MUTU['BOD5'] else 'red']
    fig.add_trace(go.Bar(x=[bod_status], y=[BOD_out_sim], marker_color=colors, text=[f"{BOD_out_sim:.1f} mg/L"], 
                        textposition='auto'), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="Dashboard Simulasi Real-time")
    st.plotly_chart(fig, use_container_width=True)

# Halaman 4: Regulatory (FIXED - Separate Indicators)
elif page == "✅ Regulatory Checker":
    st.header("✅ Regulatory Checker")
    st.markdown("**PP No. 22 Tahun 2021 - Baku Mutu Domestik**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: BOD_eff = st.number_input("**BOD5** (mg/L)", 0.0, 200.0, 25.0)
    with col2: COD_eff = st.number_input("**COD** (mg/L)", 0.0, 500.0, 80.0)
    with col3: TSS_eff = st.number_input("**TSS** (mg/L)", 0.0, 200.0, 20.0)
    with col4: pH_eff = st.number_input("**pH**", 4.0, 12.0, 7.0)
    
    if st.button("🔍 Cek Kepatuhan", type="primary"):
