import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Overview", layout="wide")

st.title("Ecosystem Overview")

try:
    with open("data/metrics/ecosystem_metrics.json", "r") as f:
        metrics = json.load(f)

    totals = metrics.get("totals", {})
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Developers", f"{totals.get('total_developers', 0):,}")
    with col2:
        st.metric("Repositories", f"{totals.get('total_repositories', 0):,}")
    with col3:
        st.metric("Total Stars", f"{totals.get('total_stars', 0):,}")
    with col4:
        st.metric("Total Forks", f"{totals.get('total_forks', 0):,}")

    st.markdown("---")

    # Load data for charts
    user_metrics = pd.read_csv("data/metrics/user_metrics.csv")
    repos = pd.read_csv("data/processed/repositories.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Developers by Influence")
        top_devs = user_metrics.sort_values(by="influence_score", ascending=False).head(
            10
        )
        st.dataframe(
            top_devs[["username", "influence_score", "total_followers"]],
            use_container_width=True,
        )

    with col2:
        st.subheader("Top 10 Repositories by Stars")
        if "stargazers_count" in repos.columns:
            top_repos = repos.sort_values(by="stargazers_count", ascending=False).head(
                10
            )
            st.dataframe(
                top_repos[["name", "stargazers_count", "language"]],
                use_container_width=True,
            )

except Exception as e:
    st.warning(
        "Data not found or error loading data. Run scripts to collect and process data."
    )
