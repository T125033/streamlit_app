import streamlit as st
import pandas as pd
import re

st.title("年齢別人口（男女別）")

df = pd.read_csv("FEH_00200524_260202185836.csv",
    encoding="shift_jis",
    header=[0, 1])

time_col = ("時間軸（年月日現在）", "時間軸（年月日現在）")
age_col  = ("年齢各歳", "年齢各歳")

def parse_year(x):
    m = re.search(r"(\d{4})年", str(x))
    return int(m.group(1)) if m else None

def parse_age(x):
    m = re.search(r"(\d+)\s*歳", str(x))
    return int(m.group(1)) if m else None

df["year"] = df[time_col].apply(parse_year)
df["age"]  = df[age_col].apply(parse_age)

