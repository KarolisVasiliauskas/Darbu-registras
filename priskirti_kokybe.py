# views/priskirti_kokybe.py
import streamlit as st
import pandas as pd
from utils import priskirti_kokybe, nuskaityti_duomenis, SLAPTAZODIS

def rodyti_kokybes_suvestine():
    slaptazodis = st.text_input("Įveskite slaptažodį", type="password")
    if slaptazodis != SLAPTAZODIS:
        st.warning("Neteisingas slaptažodis")
        return

    st.subheader("🔍 Priskirti kokybę atliktiems darbams")
    df = nuskaityti_duomenis()
    neivertinti = df[(df['Būsena'] == 'Atlikta') & (df['Kokybė'] == '')]

    if neivertinti.empty:
        st.info("Nėra užduočių be kokybės įvertinimo.")
        return

    for i, eilute in neivertinti.iterrows():
        st.markdown(f"**{eilute['Vardas']}** – {eilute['Užduotis']}")
        ivertinimas = st.slider(f"Kokybė (0–10) – ID {i}", 0, 10, key=str(i))
        if st.button("💾 Išsaugoti kokybę", key=f"save_{i}"):
            priskirti_kokybe(i, ivertinimas)
            st.success("Įvertinta")
