import streamlit as st
from chempy import balance_stoichiometry
from chempy.util.parsing import formula_to_composition
from periodictable import elements

def get_molar_mass(formula):
    comp = formula_to_composition(formula)
    return sum(elements[el].mass * n for el, n in comp.items())

st.set_page_config(page_title="Kalkulator Stoikiometri", layout="centered")
st.title("🧪 Kalkulator Stoikiometri Interaktif")
st.markdown("Hitung jumlah mol atau gram pereaksi dan produk dari reaksi kimia yang seimbang.")

st.markdown("### Pilih Reaksi atau Masukkan Sendiri")

# Daftar reaksi pilihan
preset_reactions = {
    "Pembakaran metana": "CH4 + O2 -> CO2 + H2O",
    "Pembakaran etanol": "C2H5OH + O2 -> CO2 + H2O",
    "Netralisasi HCl + NaOH": "HCl + NaOH -> NaCl + H2O",
    "Reaksi seng + HCl": "Zn + HCl -> ZnCl2 + H2",
    "Kombinasi nitrogen dan hidrogen": "N2 + H2 -> NH3",
    "Masukkan reaksi sendiri": ""
}

reaction_choice = st.selectbox("Pilih reaksi:", list(preset_reactions.keys()))
reaction_input = preset_reactions[reaction_choice]

if reaction_input == "":
    reaction_input = st.text_input("Reaksi Kimia:", "CH4 + O2 -> CO2 + H2O")
else:
    st.text_input("Reaksi Kimia:", value=reaction_input, disabled=True)

try:
    reac, prod = reaction_input.split("->")
    reac = [r.strip() for r in reac.strip().split("+")]
    prod = [p.strip() for p in prod.strip().split("+")]

    reac_dict, prod_dict = balance_stoichiometry(set(reac), set(prod))

    st.subheader("📘 Reaksi Terimbang:")
    reaksi_str = " + ".join([f"{v} {k}" for k, v in reac_dict.items()])
    reaksi_str += " → " + " + ".join([f"{v} {k}" for k, v in prod_dict.items()])
    st.success(reaksi_str)

    all_species = list(reac_dict.keys() | prod_dict.keys())
    known_substance = st.selectbox("Zat yang diketahui jumlahnya:", all_species)
    known_unit = st.radio("Satuan input:", ["mol", "gram"])
    known_value = st.number_input(f"Jumlah {known_unit}:", min_value=0.0, step=0.1)

    if known_value > 0:
        coeff_known = reac_dict.get(known_substance, prod_dict.get(known_substance))
        M_known = get_molar_mass(known_substance)
        n_known = known_value if known_unit == "mol" else known_value / M_known

        st.markdown("### 📊 Hasil Perhitungan:")
        for species in all_species:
            if species != known_substance:
                coeff_target = reac_dict.get(species, prod_dict.get(species))
                n_target = (n_known / coeff_known) * coeff_target
                M_target = get_molar_mass(species)
                mass_target = n_target * M_target

                with st.container():
                    st.markdown(f"**{species}**")
                    st.markdown(f"- Mol: `{n_target:.3f}` mol")
                    st.markdown(f"- Gram: `{mass_target:.2f}` gram")
                    st.markdown("---")

except Exception as e:
    st.error("Gagal membaca reaksi. Format harus seperti: `C2H6 + O2 -> CO2 + H2O`.")
