# views/kpi_suvestine.py
import streamlit as st
from utils import gauti_kpi_suvestine

def rodyti_kpi():
    st.subheader("📊 Komandos KPI suvestinė")
    df = gauti_kpi_suvestine()
    st.dataframe(df)
