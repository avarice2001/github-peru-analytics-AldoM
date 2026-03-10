import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Industries", layout="wide")

st.title("Industry Analysis")

try:
    class_df = pd.read_csv("data/processed/classifications.csv")

    if "industry_name" in class_df.columns:
        industry_counts = class_df["industry_name"].value_counts().reset_index()
        industry_counts.columns = ["Industry", "Count"]

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.pie(
                industry_counts,
                values="Count",
                names="Industry",
                title="Repositories by Industry",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.dataframe(industry_counts, use_container_width=True)
    else:
        st.info("Classification data format invalid.")

except FileNotFoundError:
    st.warning("Classification data not found. Please run the classification script.")
