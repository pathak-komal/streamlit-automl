import streamlit as st
import pandas as pd
import os
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from pycaret.classification import compare_models, setup, pull, save_model

with st.sidebar:
    ##st.image("")  # You can add a logo here
    st.title("AutoStreamML")
    choice = st.radio("Navigation", ["Upload", "Profiling", "ML", "Download"])
    st.info("This application allows you to build an automated ML pipeline using Streamlit.")

if os.path.exists("sourcedata.csv"):
    df = pd.read_csv("sourcedata.csv", index_col=None)

if choice == "Upload":
    st.title("Upload Your Data for Modelling!")
    file = st.file_uploader("Upload Your Dataset Here")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv("sourcedata.csv", index=None)
        st.dataframe(df)

if choice == "Profiling":
    st.title("Automated Exploratory Data Analysis")
    profile_report = ProfileReport(df, title="Profiling Report")
    st_profile_report(profile_report)

if choice == "ML":
    st.title("Machine Learning go BRR****")

    # Filter columns that are classification-suitable
    suitable_targets = []
    for col in df.columns:
        if df[col].nunique() <= len(df) * 0.5:  # avoid unique ID-like columns
            vc = df[col].value_counts(dropna=False)
            if len(vc) > 1 and vc.min() >= 2:
                suitable_targets.append(col)

    if not suitable_targets:
        st.error("No suitable target column found. Please upload a proper dataset.")
    else:
        target = st.selectbox("Select your target", suitable_targets)

        if st.button("Train Model"):
            df_cleaned = df.dropna(subset=[target])
            setup(data=df_cleaned, target=target)
            st.info("This is the ML experiment settings.")
            best_model = compare_models()
            compare_df = pull()
            st.info("This is the ML model comparison.")
            st.dataframe(compare_df)
            save_model(best_model, 'best_model')

if choice == "Download":
    with open("best_model.pkl", 'rb') as f:
        st.download_button("Download the trained model", f, "trained_model.pkl")
