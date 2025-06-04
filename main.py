# main.py
import streamlit as st
from views import registruoti_uzduoti, suvesti_darbus, priskirti_kokybe, kpi_suvestine, redaguoti_uzduotis

st.set_page_config(page_title="Komandos darbų sekimas", layout="wide")
st.title("🗂️ Komandos darbų sekimo sistema")

pagrindinis_langas = st.sidebar.selectbox(
    "Pasirinkite veiksmą:",
    (
        "📅 Dienos darbai ir registracija",
        "📝 Suvesti atliktus darbus",
        "🎯 Priskirti darbų kokybę",
        "📊 Komandos KPI",
        "✏️ Redaguoti užduotis"
    )
)

if pagrindinis_langas == "📅 Dienos darbai ir registracija":
    registruoti_uzduoti.rodyti_uzduoties_registravima()

elif pagrindinis_langas == "📝 Suvesti atliktus darbus":
    suvesti_darbus.rodyti_suvesti()

elif pagrindinis_langas == "🎯 Priskirti darbų kokybę":
    priskirti_kokybe.rodyti_kokybes_vertinima()

elif pagrindinis_langas == "📊 Komandos KPI":
    kpi_suvestine.rodyti_kpi()

elif pagrindinis_langas == "✏️ Redaguoti užduotis":
    redaguoti_uzduotis.rodyti_redagavima()
