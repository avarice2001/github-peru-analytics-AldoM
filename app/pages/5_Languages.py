import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Languages", layout="wide")

st.title("Language Analytics")

try:
    repos_df = pd.read_csv("data/processed/repositories.csv")

    if "language" in repos_df.columns:
        language_counts = repos_df["language"].dropna().value_counts().reset_index()
        language_counts.columns = ["Language", "Count"]

        # Take top 15
        top_languages = language_counts.head(15)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.bar(
                top_languages,
                x="Language",
                y="Count",
                title="Top 15 Programming Languages",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.dataframe(language_counts, use_container_width=True)
    else:
        st.info("Language data not available.")

except FileNotFoundError:
    st.warning("Repository data not found. Please run the data pipelines.")
