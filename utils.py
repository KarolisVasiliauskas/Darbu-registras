# utils.py
import pandas as pd
from datetime import datetime

FAILAS = "duomenys.csv"
SLAPTAZODIS = "slaptas"

STULPELIAI = ["Data", "Vardas", "Užduotis", "Trukmė_h", "Būsena", "Kokybė"]


def nuskaityti_duomenis():
    try:
        df = pd.read_csv(FAILAS)
    except FileNotFoundError:
        df = pd.DataFrame(columns=STULPELIAI)
    return df


def issaugoti_duomenis(df):
    df.to_csv(FAILAS, index=False)


def irasyti_darba(vardas, data, uzduotis, trukme):
    df = nuskaityti_duomenis()
    naujas = {
        "Data": data.strftime("%Y-%m-%d"),
        "Vardas": vardas,
        "Užduotis": uzduotis,
        "Trukmė_h": trukme,
        "Būsena": "Vykdoma",
        "Kokybė": ""
    }
    df = pd.concat([df, pd.DataFrame([naujas])], ignore_index=True)
    issaugoti_duomenis(df)


def redaguoti_uzduoti(indeksas, trukme, busena):
    df = nuskaityti_duomenis()
    df.at[indeksas, "Trukmė_h"] = trukme
    df.at[indeksas, "Būsena"] = busena
    issaugoti_duomenis(df)


def priskirti_kokybe(indeksas, ivertinimas):
    df = nuskaityti_duomenis()
    df.at[indeksas, "Kokybė"] = ivertinimas
    issaugoti_duomenis(df)


def perleisti_uzduoti(indeksas, naujas_vardas):
    df = nuskaityti_duomenis()
    df.at[indeksas, "Vardas"] = naujas_vardas
    issaugoti_duomenis(df)


def istrinti_uzduoti(indeksas):
    df = nuskaityti_duomenis()
    df = df.drop(index=indeksas)
    df.reset_index(drop=True, inplace=True)
    issaugoti_duomenis(df)


def gauti_kpi_suvestine():
    df = nuskaityti_duomenis()
    if df.empty:
        return df
    return df.groupby("Vardas").agg({
        "Užduotis": "count",
        "Trukmė_h": "sum",
        "Kokybė": lambda x: pd.to_numeric(x, errors='coerce').mean()
    }).rename(columns={"Užduotis": "Užduocių sk.", "Trukmė_h": "Valandos", "Kokybė": "Vid. kokybė"})


def gauti_darbuotoju_sarasa():
    df = nuskaityti_duomenis()
    return sorted(df['Vardas'].dropna().unique().tolist())
