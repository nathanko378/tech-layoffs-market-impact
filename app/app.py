import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

cols = ["# Laid Off","% Laid Off","Date Added","Ticker","$ Change 5D","% Change 5D", "$ Change 1Y", "% Change 1Y"]
layoff_vs_immediate_df = pd.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate_updated.csv", usecols=cols)
layoff_vs_immediate_df['% Laid Off'] = layoff_vs_immediate_df['% Laid Off'].str.replace('%', '').astype(float)


st.set_page_config(
    page_title="Stock peer analysis dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :violet[:material/query_stats: Tech Layoffs & Market Impact (2021-2025)]

Interactive dashboard exploring the relationship between major tech layoffs and stockholder value.

 **Data sources:** Layoffs.fyi & Yahoo Finance
"""
"""





"""

col1, col2 = st.columns([1, 2])  # left = description, right = plot

with col1:
    st.markdown("""
    ## Top Layoff Events vs. Immediate Stock Impact
    **Description**  
    This scatter plot compares the **percentage of workforce laid off** (`% Laid Off`)  
    against the **immediate 5-day stock price change** (`% Change 5D`).  
    - Each point represents a company layoff event.  
    - Helps visualize whether larger layoffs correlate with stronger immediate stock reactions.
    """)

with col2:
    scatter = alt.Chart(layoff_vs_immediate_df).mark_circle(size=80, opacity=0.7).encode(
        x=alt.X("% Laid Off", title="% Workforce Laid Off"),
        y=alt.Y("% Change 5D", title="% Change in Stock (5D)"),
        tooltip=cols
    ).properties(
        width=500,
        height=400
    )
    st.altair_chart(scatter, use_container_width=True)

"""
## Raw data
"""

layoff_vs_immediate_df