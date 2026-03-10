import streamlit as st
import pandas as pd

st.set_page_config(page_title="Repositories", layout="wide")

st.title("Repository Browser")

try:
    repos = pd.read_csv("data/processed/repositories.csv")
    classifications = pd.read_csv("data/processed/classifications.csv")

    # Combine
    if "repo_id" in classifications.columns and "id" in repos.columns:
        display_df = pd.merge(
            repos, classifications, left_on="id", right_on="repo_id", how="left"
        )
    else:
        display_df = repos

    # Filters
    st.sidebar.header("Filters")

    search_term = st.sidebar.text_input("Search by name/description")

    langs = ["All"] + list(display_df["language"].dropna().unique())
    selected_lang = st.sidebar.selectbox("Language", langs)

    min_stars = st.sidebar.slider(
        "Min Stars",
        0,
        int(
            display_df["stargazers_count"].max()
            if "stargazers_count" in display_df.columns
            else 1000
        ),
        0,
    )

    filtered_df = display_df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_term, case=False, na=False)
            | filtered_df["description"].str.contains(search_term, case=False, na=False)
        ]

    if selected_lang != "All":
        filtered_df = filtered_df[filtered_df["language"] == selected_lang]

    if "stargazers_count" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["stargazers_count"] >= min_stars]

    st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.warning("Data not found. Please run the data pipelines.")
