import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
from fpdf import FPDF

@st.cache_data
def load_data():
    df = pd.read_excel("RSG CONFIGURATOR UPLOAD 2.0.xlsx", sheet_name="Sheet1")
    df["APPLICATION"] = df["APPLICATION"].astype(str)
    if "Industrial" not in df["APPLICATION"].unique():
        df = pd.concat([df, pd.DataFrame([{**{col: None for col in df.columns}, "APPLICATION": "Industrial"}])], ignore_index=True)
    return df

df = load_data()

theme = st.sidebar.radio("Choose Theme", ["Light Mode", "Dark Mode"])
if theme == "Dark Mode":
    st.markdown("""
    <style>
        .stApp { background-color: #111; color: #f0f0f0; }
        h1, h2, h3 { color: #CC0000; }
        .stButton>button {
            background-color: #CC0000; color: white; padding: 0.5em 1em;
            border-radius: 6px; border: none; font-weight: bold;
        }
        .stButton>button:hover { background-color: #A80000; }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp { background-color: white; font-family: Arial, sans-serif; }
        h1, h2, h3 { color: #CC0000; }
        .stButton>button {
            background-color: #CC0000; color: white; padding: 0.5em 1em;
            border-radius: 6px; border: none; font-weight: bold;
        }
        .stButton>button:hover { background-color: #A80000; }
    </style>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 6, 2])
with col1:
    st.image("Cummins logo.png", width=80)
with col2:
    st.markdown("<h1 style='text-align: center;'>RSG Fuel System Configurator</h1>", unsafe_allow_html=True)
with col3:
    st.image("republic_logo.png", width=80)

def get_options(column):
    opts = df[column].dropna().unique().tolist()
    opts = sorted(set(opts))
    return ["Please Select"] + opts

application = st.selectbox("Select Application Type", get_options("APPLICATION"))
filtered_df = df if application == "Please Select" else df[df["APPLICATION"] == application]

body_mfg = st.selectbox("Select Body Manufacturer", get_options("BODY MFG"))
filtered_df = filtered_df if body_mfg == "Please Select" else filtered_df[filtered_df["BODY MFG"] == body_mfg]

chassis_mfg = st.selectbox("Select Chassis Manufacturer", get_options("CHASSIS MANUFACTURE"))
filtered_df = filtered_df if chassis_mfg == "Please Select" else filtered_df[filtered_df["CHASSIS MANUFACTURE"] == chassis_mfg]

chassis_model = st.selectbox("Select Chassis Model", get_options("CHASSIS MODEL"))
filtered_df = filtered_df if chassis_model == "Please Select" else filtered_df[filtered_df["CHASSIS MODEL"] == chassis_model]

chassis_cab = st.selectbox("Select Chassis Cab", get_options("CHASSIS CAB"))
filtered_df = filtered_df if chassis_cab == "Please Select" else filtered_df[filtered_df["CHASSIS CAB"] == chassis_cab]

cng_mount = st.selectbox("Select CNG Mounting", get_options("CNG MOUNTING"))
filtered_df = filtered_df if cng_mount == "Please Select" else filtered_df[filtered_df["CNG MOUNTING"] == cng_mount]

system_dge = st.selectbox("Select System DGE", get_options("SYSTEM DGE"))
filtered_df = filtered_df if system_dge == "Please Select" else filtered_df[filtered_df["SYSTEM DGE"] == system_dge]

st.markdown("### Matching Configurations")
st.dataframe(filtered_df.reset_index(drop=True))

st.markdown("### Export Results")
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    return output.getvalue()

def convert_df_to_pdf(df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for col in df.columns:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, str(item)[:15], border=1)
        pdf.ln()
    output = BytesIO()
    pdf.output(output)
    return output.getvalue()

if not filtered_df.empty:
    excel_data = convert_df_to_excel(filtered_df)
    pdf_data = convert_df_to_pdf(filtered_df)
    st.download_button("Download as Excel", excel_data, "filtered_results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("Download as PDF", pdf_data, "filtered_results.pdf", "application/pdf")
else:
    st.info("No results available to download.")

st.markdown("---")
st.markdown("**Embed Ready:** This app is iframe-compatible for Salesforce Community and dealer portals.")
