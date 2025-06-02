# views/suvesti_darbus.py
import streamlit as st
import pandas as pd
from utils import nuskaityti_duomenis, redaguoti_uzduoti

def rodyti_suvesti_darbus():
    st.subheader("✅ Suvesti atliktus darbus")
    df = nuskaityti_duomenis()

    vardas = st.selectbox("Pasirinkite darbuotoją:", sorted(df['Vardas'].dropna().unique().tolist()))
    uzduotys = df[(df['Vardas'] == vardas) & (df['Būsena'] != 'Atlikta')]

    pasirinkta = st.selectbox("Užduotis:", uzduotys['Užduotis'].tolist())
    eil = uzduotys[uzduotys['Užduotis'] == pasirinkta].index[0]
    trukme = st.number_input("Trukmė (valandomis)", min_value=0.0, step=0.5)

    if st.button("💾 Išsaugoti"):
        redaguoti_uzduoti(eil, trukme, "Vykdoma")
        st.success("Trukmė išsaugota")

    if st.button("🏁 Projektas baigtas"):
        redaguoti_uzduoti(eil, trukme, "Atlikta")
        st.success("Užduotis pažymėta kaip atlikta")
