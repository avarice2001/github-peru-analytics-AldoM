import streamlit as st
import pandas as pd

st.set_page_config(page_title="Developers", layout="wide")

st.title("Developer Explorer")

try:
    user_metrics = pd.read_csv("data/metrics/user_metrics.csv")
    users_raw = pd.read_csv("data/processed/users.csv")

    # Merge for display
    display_df = pd.merge(
        user_metrics,
        users_raw[["login", "name", "company", "location"]],
        left_on="username",
        right_on="login",
        how="left",
    )
    display_df = display_df.drop(columns=["login"])

    # Filters
    st.sidebar.header("Filters")
    min_followers = st.sidebar.slider(
        "Min Followers",
        0,
        int(display_df["total_followers"].max() if not display_df.empty else 100),
        0,
    )

    filtered_df = display_df[display_df["total_followers"] >= min_followers]

    st.dataframe(filtered_df, use_container_width=True)

    st.download_button(
        label="Download data as CSV",
        data=filtered_df.to_csv().encode("utf-8"),
        file_name="developer_metrics.csv",
        mime="text/csv",
    )

except FileNotFoundError:
    st.warning("User metrics data not found. Please run the data pipelines.")
