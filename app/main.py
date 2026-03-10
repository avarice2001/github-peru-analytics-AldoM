import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="GitHub Peru Analytics",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("GitHub Peru Analytics Dashboard")
st.markdown("""
Welcome to the GitHub Peru Analytics Dashboard! 
This platform provides insights into the Peruvian developer ecosystem, analyzing repositories, developers, industries, and programming languages.
Use the sidebar to navigate through the different views.
""")

# Load overview stats
try:
    with open("data/metrics/ecosystem_metrics.json", "r") as f:
        metrics = json.load(f)

    totals = metrics.get("totals", {})
    st.header("Ecosystem Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Developers", f"{totals.get('total_developers', 0):,}")
    with col2:
        st.metric("Total Repositories", f"{totals.get('total_repositories', 0):,}")
    with col3:
        st.metric("Total Stars", f"{totals.get('total_stars', 0):,}")
    with col4:
        st.metric("Total Forks", f"{totals.get('total_forks', 0):,}")

except FileNotFoundError:
    st.warning(
        "Data not found. Please run the extraction, classification, and metrics scripts first."
    )
