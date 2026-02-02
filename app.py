import streamlit as st
import pandas as pd
import re

st.title("年齢別人口（男女別）のグラフ")

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

years = sorted(df["year"].unique())

with st.sidebar:
    year = st.selectbox("西暦を選択", years)
    
    sex = st.pills(
        "性別を選択",
        options=["男", "女"],
        selection_mode="single",
        default="男"
    )

    show_table = st.toggle("表を表示する（OFFでグラフを表示）", value=False)

sex_col = ("総人口", f"{sex}【千人】")

dff = df[(df["year"] == year) & (df["age"].notna())].copy()

dff["pop"] = pd.to_numeric(
    dff[sex_col].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)

out = (
    dff[["age", "pop"]]
    .sort_values("age")
    .set_index("age")
)
out.columns = [f"{sex}性（千人）"]

st.caption("単位：千人")

if show_table:
    st.dataframe(out, height=450)
else:
    st.subheader(f"{year}年：{sex}性の年齢別人口（総人口）")
    st.line_chart(out)
