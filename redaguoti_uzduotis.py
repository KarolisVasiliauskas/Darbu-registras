# views/redaguoti_uzduotis.py
import streamlit as st
from utils import nuskaityti_duomenis, redaguoti_uzduoti, perleisti_uzduoti, istrinti_uzduoti

def rodyti_redagavima():
    st.subheader("✏️ Redaguoti užduotis")
    df = nuskaityti_duomenis()
    aktyvios = df[df['Būsena'] != 'Atlikta']

    if aktyvios.empty:
        st.info("Nėra aktyvių užduočių.")
        return

    pasirinkimas = st.selectbox("Pasirinkite užduotį:", aktyvios['Užduotis'].tolist())
    uzduotis = aktyvios[aktyvios['Užduotis'] == pasirinkimas].iloc[0]
    indeksas = aktyvios[aktyvios['Užduotis'] == pasirinkimas].index[0]

    trukme = st.number_input("Skirtas laikas (val.)", value=float(uzduotis['Trukmė_h']), step=0.5)
    busena = st.selectbox("Būsena:", ["Vykdoma", "Atlikta"], index=["Vykdoma", "Atlikta"].index(uzduotis['Būsena']))

    if st.button("💾 Išsaugoti pakeitimus"):
        redaguoti_uzduoti(indeksas, trukme, busena)
        st.success("Atnaujinta")

    if st.button("➡️ Perleisti užduotį kitam"):
        naujas = st.text_input("Naujas darbuotojas")
        if naujas:
            perleisti_uzduoti(indeksas, naujas)
            st.success("Perleista")

    if st.button("🗑️ Ištrinti užduotį"):
        istrinti_uzduoti(indeksas)
        st.success("Ištrinta")
