# app.py
import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = "duomenys.csv"
SLAPTAZODIS = "slaptas"

# Inicializuojam failą jei jo nėra
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Vardas", "Data", "Užduotis", "Trukmė_h", "Kokybė", "Būsena"])
        df.to_csv(DATA_FILE, index=False)

# Užrašo į naują eilutę
def irasyti_darba(vardas, data, uzduotis, trukme):
    df = pd.read_csv(DATA_FILE)
    naujas = pd.DataFrame([{
        "Vardas": vardas,
        "Data": data.strftime("%Y-%m-%d"),
        "Užduotis": uzduotis,
        "Trukmė_h": trukme,
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
def redaguoti_uzduoti(eilutes_id, trukme, busena):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Trukmė_h"] = trukme
    df.loc[eilutes_id, "Būsena"] = busena
    df.to_csv(DATA_FILE, index=False)

# Skaičiuoja KPI
def gauti_kpi_suvestine():
    df = pd.read_csv(DATA_FILE)
    df = df[df["Kokybė"] != ""]
    df["Trukmė_h"] = pd.to_numeric(df["Trukmė_h"], errors='coerce')
    df["Kokybė"] = pd.to_numeric(df["Kokybė"], errors='coerce')
    df["Greitis"] = 1 / df["Trukmė_h"]
    return df.groupby("Vardas").agg({
        "Trukmė_h": "sum",
        "Greitis": "mean",
        "Kokybė": "mean"
    }).round(2).reset_index()

# Pagrindinis
init_data_file()
st.title("📅 Komandos darbų ir KPI sekimas")

diena = st.date_input("Pasirinkite datą", value=datetime.date.today())
df = pd.read_csv(DATA_FILE)
visi_vardai = sorted(df["Vardas"].dropna().unique().tolist())

# Filtravimas
st.subheader("🔍 Filtrai")
col1, col2 = st.columns(2)
with col1:
    pasirinktas_vardas = st.selectbox("Filtruoti pagal vardą", ["Visi"] + visi_vardai)
with col2:
    pasirinkta_busena = st.selectbox("Filtruoti pagal būseną", ["Visos", "Vykdoma", "Atlikta"])

filtruoti = df[df["Data"] == diena.strftime("%Y-%m-%d")]
if pasirinktas_vardas != "Visi":
    filtruoti = filtruoti[filtruoti["Vardas"] == pasirinktas_vardas]
if pasirinkta_busena != "Visos":
    filtruoti = filtruoti[filtruoti["Būsena"] == pasirinkta_busena]

st.subheader(f"Darbai {diena}")
st.dataframe(filtruoti, use_container_width=True)

st.markdown("---")

option = st.radio("Pasirinkite veiksmą:", [
    "🗂 Užregistruoti užduotį",
    "📄 Suvesti atliktus darbus",
    "✏️ Redaguoti užduotis",
    "🔍 Priskirti darbų kokybę",
    "📊 Peržiūrėti komandos KPI"
])

if option == "📄 Suvesti atliktus darbus":
    st.subheader("✏️ Naujo darbo registracija")
    vardas = st.selectbox("Vardas", visi_vardai)
    uzduociu_sarasas = df[(df["Vardas"] == vardas) & (df["Būsena"] == "Vykdoma")]["Užduotis"].unique().tolist()
    uzduotis = st.selectbox("Užduotis", uzduociu_sarasas)
    trukme = st.number_input("Trukmė (val.)", min_value=0.0, step=0.25)
    cols = st.columns([1, 1])
    if cols[0].button("➕ Išsaugoti"):
        if vardas and uzduotis:
            irasyti_darba(vardas, datetime.datetime.now(), uzduotis, trukme)
            st.success("Darbas įregistruotas")
            st.experimental_rerun()
        else:
            st.warning("Užpildykite visus laukus")
    if cols[1].button("✅ Projektas baigtas"):
        df_idx = df[(df["Vardas"] == vardas) & (df["Užduotis"] == uzduotis) & (df["Būsena"] == "Vykdoma")].index
        if not df_idx.empty:
            redaguoti_uzduoti(df_idx[0], trukme, "Atlikta")
            st.success("Užduotis pažymėta kaip atlikta")
            st.experimental_rerun()

elif option == "✏️ Redaguoti užduotis":
    st.subheader("🛠️ Redaguoti esamas užduotis")
    for i, row in df[df["Būsena"] == "Vykdoma"].iterrows():
        st.markdown(f"**{row['Data']} – {row['Vardas']} – {row['Užduotis']}**")
        new_trukme = st.number_input(f"Trukmė #{i}", value=float(row["Trukmė_h"]), key=f"trukme_{i}")
        new_busena = st.selectbox(f"Būsena #{i}", ["Vykdoma", "Atlikta"], index=0 if row["Būsena"] != "Atlikta" else 1, key=f"busena_{i}")
        cols = st.columns([2, 2, 2])
        if cols[0].button(f"💾 Išsaugoti pakeitimus #{i}", key=f"save_{i}"):
            redaguoti_uzduoti(i, new_trukme, new_busena)
            st.success("Užduotis atnaujinta")
            st.experimental_rerun()
        if cols[1].button(f"🔁 Perleisti užduotį #{i}", key=f"perleisti_{i}"):
            naujas_vardas = st.selectbox(f"Pasirinkite kam perleisti #{i}", visi_vardai, key=f"naujas_vardas_{i}")
            perleisti_uzduoti(i, naujas_vardas)
            st.success("Užduotis perleista")
            st.experimental_rerun()
        if cols[2].button(f"🗑️ Ištrinti užduotį #{i}", key=f"istrinti_{i}"):
            istrinti_uzduoti(i)
            st.success("Užduotis ištrinta")
            st.experimental_rerun()

elif option == "🔍 Priskirti darbų kokybę":
    slaptazodis = st.text_input("Įveskite slaptažodį", type="password")
    if slaptazodis == SLAPTAZODIS:
        st.subheader("🔬 Neįvertinti darbai")
        df = pd.read_csv(DATA_FILE)
        neivertinti = df[(df["Kokybė"] == "") & (df["Būsena"] == "Vykdoma")]
        for i, row in neivertinti.iterrows():
            st.markdown(f"**{row['Data']} – {row['Vardas']}: {row['Užduotis']}**")
            ivert = st.slider(f"Kokybė darbui #{i}", min_value=0, max_value=100, key=f"kokybe_{i}")
            if st.button(f"🔄 Priskirti #{i}", key=f"btn_{i}"):
                priskirti_kokybe(i, ivert)
                st.success("Kokybė priskirta")
                st.experimental_rerun()
    elif slaptazodis:
        st.error("Neteisingas slaptažodis")

elif option == "📊 Peržiūrėti komandos KPI":
    st.subheader("Komandos KPI suvestinė")
    kpi = gauti_kpi_suvestine()
    st.dataframe(kpi, use_container_width=True)

elif option == "🗂 Užregistruoti užduotį":
    st.subheader("🗓️ Užduoties registracija")
    vardas = st.selectbox("Darbuotojo vardas", visi_vardai)
    uzduotis = st.text_input("Užduotis")
    data = st.date_input("Užduoties data")
    trukme = st.number_input("Skirtas laikas (val.)", min_value=0.0, step=0.25)
    if st.button("📌 Registruoti užduotį"):
        if vardas and uzduotis:
            irasyti_darba(vardas, data, uzduotis, trukme)
            st.success("Užduotis užregistruota")
        else:
            st.warning("Užpildykite visus laukus")
