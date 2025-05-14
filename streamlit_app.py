import streamlit as st
from sympy import symbols, Eq, solve
from chempy import balance_stoichiometry
from chempy.util.parsing import formula_to_composition

st.set_page_config(page_title="Kalkulator Stoikiometri", layout="centered")

st.title("Kalkulator Stoikiometri Reaksi Kimia")
st.markdown("Masukkan reaksi kimia, contoh: `H2 + O2 -> H2O`")

# Input reaksi
reaction_input = st.text_input("Reaksi:", "H2 + O2 -> H2O")

try:
    reac, prod = reaction_input.split("->")
    reac = reac.strip().split("+")
    prod = prod.strip().split("+")
    reac = [r.strip() for r in reac]
    prod = [p.strip() for p in prod]

    reac_dict, prod_dict = balance_stoichiometry(set(reac), set(prod))

    st.subheader("Reaksi Terimbang:")
    reaksi_str = " + ".join([f"{v} {k}" for k, v in reac_dict.items()])
    reaksi_str += " → " + " + ".join([f"{v} {k}" for k, v in prod_dict.items()])
    st.success(reaksi_str)

    st.subheader("Hitung Stoikiometri")
    known_substance = st.selectbox("Zat yang diketahui jumlahnya:", list(reac_dict.keys()) + list(prod_dict.keys()))
    known_amount = st.number_input("Jumlah (mol):", min_value=0.0, step=0.1)

    if known_amount > 0:
        coeff_known = reac_dict.get(known_substance, prod_dict.get(known_substance))
        
        st.markdown("### Hasil Perhitungan (mol):")
        for species in reac_dict | prod_dict:
            if species != known_substance:
                coeff_target = reac_dict.get(species, prod_dict.get(species))
                amount = (known_amount / coeff_known) * coeff_target
                st.write(f"{species}: {amount:.2f} mol")

except Exception as e:
    st.error("Gagal membaca reaksi. Pastikan formatnya benar, misalnya: `CH4 + O2 -> CO2 + H2O`.")
