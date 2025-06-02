# utils.py
import os
import pandas as pd
import datetime

DATA_FILE = "duomenys.csv"
SLAPTAZODIS = "slaptas"

def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Vardas", "Data", "Užduotis", "Trukmė_h", "Kokybė", "Būsena"])
        df.to_csv(DATA_FILE, index=False)

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

def priskirti_kokybe(eilutes_id, kokybe):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Kokybė"] = kokybe
    df.to_csv(DATA_FILE, index=False)

def redaguoti_uzduoti(eilutes_id, trukme, busena):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Trukmė_h"] = trukme
    df.loc[eilutes_id, "Būsena"] = busena
    df.to_csv(DATA_FILE, index=False)

def perleisti_uzduoti(eilutes_id, naujas_vardas):
    df = pd.read_csv(DATA_FILE)
    df.loc[eilutes_id, "Vardas"] = naujas_vardas
    df.to_csv(DATA_FILE, index=False)

def istrinti_uzduoti(eilutes_id):
    df = pd.read_csv(DATA_FILE)
    df = df.drop(index=eilutes_id)
    df.to_csv(DATA_FILE, index=False)

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

def nuskaityti_duomenis():
    return pd.read_csv(DATA_FILE)
