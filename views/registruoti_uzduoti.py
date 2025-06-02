# views/registruoti_uzduoti.py
import streamlit as st
import pandas as pd
from utils import irasyti_darba, nuskaityti_duomenis
from datetime import datetime

def rodyti_uzduoties_registravima():
    st.subheader("📝 Užregistruoti naują užduotį")
    vardas = st.selectbox("Pasirinkite darbuotoją:", gauti_darbuotoju_sarasa())
    uzduotis = st.text_input("Užduoties aprašymas")
    skirtas_laikas = st.number_input("Skirtas laikas (valandomis)", min_value=0.0, step=0.5)
    if st.button("💾 Išsaugoti užduotį"):
        if vardas and uzduotis:
            irasyti_darba(vardas, datetime.today(), uzduotis, skirtas_laikas)
            st.success("Užduotis išsaugota.")

def rodyti_dienos_darbus():
    st.subheader("📆 Pasirinktos dienos darbai")
    df = nuskaityti_duomenis()
    pasirinkta_data = st.date_input("Pasirinkite datą:", value=datetime.today())
    filtroti = df[df['Data'] == pasirinkta_data.strftime("%Y-%m-%d")]
    st.dataframe(filtroti)

def gauti_darbuotoju_sarasa():
    df = nuskaityti_duomenis()
    return sorted(df['Vardas'].dropna().unique().tolist())
