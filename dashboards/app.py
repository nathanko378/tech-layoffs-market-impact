import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tech Layoffs & Market Impact (2025)", layout="wide")

#Title and Description
st.title("📉 :violet[Tech Layoffs & Market Impact (2025)]")
st.markdown(
    """
    Interactive dashboard exploring the relationship between major tech layoffs and stockholder value.

    **Data sources:** Layoffs.fyi & Yahoo Finance  
    """
)