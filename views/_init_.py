# views/__init__.py
import streamlit as st
from views import registruoti_uzduoti, suvesti_darbus, priskirti_kokybe, kpi_suvestine, redaguoti_uzduotis

def show_main_view():
    st.title("📅 Komandos darbų ir KPI sekimas")

    pasirinkimas = st.sidebar.radio("Pasirinkite skiltį:", (
        "📆 Dienos darbai",
        "📝 Užregistruoti užduotį",
        "✅ Suvesti atliktus darbus",
        "🔍 Priskirti darbų kokybę",
        "📊 Komandos KPI",
        "✏️ Redaguoti užduotis"
    ))

    if pasirinkimas == "📆 Dienos darbai":
        registruoti_uzduoti.rodyti_dienos_darbus()
    elif pasirinkimas == "📝 Užregistruoti užduotį":
        registruoti_uzduoti.rodyti_uzduoties_registravima()
    elif pasirinkimas == "✅ Suvesti atliktus darbus":
        suvesti_darbus.rodyti_suvesti_darbus()
    elif pasirinkimas == "🔍 Priskirti darbų kokybę":
        priskirti_kokybe.rodyti_kokybes_suvestine()
    elif pasirinkimas == "📊 Komandos KPI":
        kpi_suvestine.rodyti_kpi()
    elif pasirinkimas == "✏️ Redaguoti užduotis":
        redaguoti_uzduotis.rodyti_redagavima()
