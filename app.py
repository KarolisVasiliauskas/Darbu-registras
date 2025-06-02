# app.py
import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = "duomenys.csv"

# Inicializuojam failą jei jo nėra
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Vardas", "Data", "Užduotis", "Trukmė_h", "Kiekis", "Kokybė", "Būsena"])
        df.to_csv(DATA_FILE, index=False)

# Užrašo į naują eilutę

def irasyti_darba(vardas, data, uzduotis, trukme, kiekis):
    df = pd.read_csv(DATA_FILE)
    naujas = pd.DataFrame([{
        "Vardas": vardas,
        "Data": data.strftime("%Y-%m-%d"),
        "Užduotis": uzduotis,
        "Trukmė_h": trukme,
        "Kiekis": kiekis,
        "Kokybė": "",
        "Būsena": "Vykdoma"
    }])
    df = pd.concat([df, naujas], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Priskiria kokybę darbui

def priskirti_kokybe(eilutes_id, kokybe):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Kokybė"] = kokybe
    df.to_csv(DATA_FILE, index=False)

# Atnaujina užduoties informaciją

def redaguoti_uzduoti(eilutes_id, trukme, kiekis, busena):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Trukmė_h"] = trukme
    df.loc[eilutes_id, "Kiekis"] = kiekis
    df.loc[eilutes_id, "Būsena"] = busena
    df.to_csv(DATA_FILE, index=False)

# Skaičiuoja KPI

def gauti_kpi_suvestine():
    df = pd.read_csv(DATA_FILE)
    df = df[df["Kokybė"] != ""]
    df["Trukmė_h"] = pd.to_numeric(df["Trukmė_h"], errors='coerce')
    df["Kiekis"] = pd.to_numeric(df["Kiekis"], errors='coerce')
    df["Kokybė"] = pd.to_numeric(df["Kokybė"], errors='coerce')
    df["Greitis"] = df["Kiekis"] / df["Trukmė_h"]
    return df.groupby("Vardas").agg({
        "Kiekis": "sum",
        "Trukmė_h": "sum",
        "Greitis": "mean",
        "Kokybė": "mean"
    }).round(2).reset_index()

# Pagrindinis
init_data_file()
st.title("📅 Komandos darbų ir KPI sekimas")

diena = st.date_input("Pasirinkite datą", value=datetime.date.today())
df = pd.read_csv(DATA_FILE)

# Filtravimas
st.subheader("🔍 Filtrai")
col1, col2 = st.columns(2)
with col1:
    pasirinktas_vardas = st.selectbox("Filtruoti pagal vardą", ["Visi"] + sorted(df["Vardas"].unique().tolist()))
with col2:
    pasirinkta_busena = st.selectbox("Filtruoti pagal būseną", ["Visos", "Vykdoma", "Atlikta"])

filtruoti = df[df["Data"] == diena.strftime("%Y-%m-%d")]
if pasirinktas_vardas != "Visi":
    filtruoti = filtruoti[filtruoti["Vardas"] == pasirinktas_vardas]
if pasirinkta_busena != "Visos":
    filtruoti = filtruoti[filtruoti["Būsena"] == pasirinkta_busena]

# Rodomas pasirinktos dienos darbų sąrašas
st.subheader(f"Darbai {diena}")
st.dataframe(filtruoti, use_container_width=True)

st.markdown("---")

# Navigacija
option = st.radio("Pasirinkite veiksmą:", [
    "🗂 Užregistruoti užduotį",
    "📄 Suvesti atliktus darbus",
    "✏️ Redaguoti užduotis",
    "🔍 Priskirti darbų kokybę",
    "📊 Peržiūrėti komandos KPI"
])

if option == "📄 Suvesti atliktus darbus":
    st.subheader("✏️ Naujo darbo registracija")
    vardas = st.text_input("Vardas")
    uzduotis = st.text_input("Užduotis")
    trukme = st.number_input("Trukmė (val.)", min_value=0.0, step=0.25)
    kiekis = st.number_input("Kiekis", min_value=0, step=1)
    if st.button("➕ Išsaugoti"):
        if vardas and uzduotis:
            irasyti_darba(vardas, datetime.datetime.now(), uzduotis, trukme, kiekis)
            st.success("Darbas įregistruotas")
        else:
            st.warning("Užpildykite visus laukus")

elif option == "✏️ Redaguoti užduotis":
    st.subheader("🛠️ Redaguoti esamas užduotis")
    for i, row in df.iterrows():
        st.markdown(f"**{row['Data']} – {row['Vardas']} – {row['Užduotis']}**")
        new_trukme = st.number_input(f"Trukmė #{i}", value=float(row["Trukmė_h"]), key=f"trukme_{i}")
        new_kiekis = st.number_input(f"Kiekis #{i}", value=int(row["Kiekis"]), key=f"kiekis_{i}")
        new_busena = st.selectbox(f"Būsena #{i}", ["Vykdoma", "Atlikta"], index=0 if row["Būsena"] != "Atlikta" else 1, key=f"busena_{i}")
        if st.button(f"💾 Išsaugoti pakeitimus #{i}", key=f"save_{i}"):
            redaguoti_uzduoti(i, new_trukme, new_kiekis, new_busena)
            st.success("Užduotis atnaujinta")
            st.experimental_rerun()

elif option == "🔍 Priskirti darbų kokybę":
    st.subheader("🔬 Neįvertinti darbai")
    df = pd.read_csv(DATA_FILE)
    neivertinti = df[df["Kokybė"] == ""]
    for i, row in neivertinti.iterrows():
        st.markdown(f"**{row['Data']} – {row['Vardas']}: {row['Užduotis']}**")
        ivert = st.slider(f"Kokybė darbui #{i}", min_value=0, max_value=100, key=f"kokybe_{i}")
        if st.button(f"🔄 Priskirti #{i}", key=f"btn_{i}"):
            priskirti_kokybe(i, ivert)
            st.success("Kokybė priskirta")
            st.experimental_rerun()

elif option == "📊 Peržiūrėti komandos KPI":
    st.subheader("Komandos KPI suvestinė")
    kpi = gauti_kpi_suvestine()
    st.dataframe(kpi, use_container_width=True)

elif option == "🗂 Užregistruoti užduotį":
    st.subheader("🗓️ Užduoties registracija")
    vardas = st.text_input("Darbuotojo vardas")
    uzduotis = st.text_input("Užduotis")
    data = st.date_input("Užduoties data")
    trukme = st.number_input("Numatoma trukmė (val.)", min_value=0.0, step=0.25)
    kiekis = st.number_input("Numatomas kiekis", min_value=0, step=1)
    if st.button("📌 Registruoti užduotį"):
        if vardas and uzduotis:
            irasyti_darba(vardas, data, uzduotis, trukme, kiekis)
            st.success("Užduotis užregistruota")
        else:
            st.warning("Užpildykite visus laukus")
