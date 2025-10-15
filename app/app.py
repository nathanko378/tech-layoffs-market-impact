import streamlit as st
import pandas as pd
import altair as alt

# --- Load and preprocess data ---
cols = ["# Laid Off", "% Laid Off", "Date Added", "Ticker", "$ Change 5D", "% Change 5D", "$ Change 1Y", "% Change 1Y"]
layoff_vs_immediate_df = pd.read_csv(
    "/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate_updated.csv",
    usecols=cols
)
layoff_vs_immediate_df['% Laid Off'] = layoff_vs_immediate_df['% Laid Off'].str.replace('%', '').astype(float)

# --- Streamlit page setup ---
st.set_page_config(
    page_title="Tech Layoffs & Market Impact Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# --- Title section ---
st.title(":violet[:material/query_stats: Tech Layoffs & Market Impact (2021–2025)]")
st.markdown("""
Interactive dashboard exploring the relationship between **major tech layoffs** and **stock performance**  
over different time horizons.

**Data sources:** Layoffs.fyi & Yahoo Finance
""")

st.markdown("---")

# =============================
# SECTION 1: Immediate Stock Impact (5D)
# =============================

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
    ## Top Layoff Events vs. Immediate Stock Impact
    **Description**
    This scatter plot compares the **percentage of workforce laid off** (`% Laid Off`)
    against the **immediate 5-day stock price change** (`% Change 5D`).
    - Each point represents a company layoff event.
    - Helps visualize whether larger layoffs correlate with stronger *short-term* market reactions.
    """)

with col2:
    scatter_5d = (
        alt.Chart(layoff_vs_immediate_df)
        .mark_circle(size=80, opacity=0.7, color="#7C3AED")
        .encode(
            x=alt.X("% Laid Off", title="% Workforce Laid Off"),
            y=alt.Y("% Change 5D", title="% Change in Stock (5D)"),
            tooltip=cols
        )
        .properties(width=550, height=400)
    )
    st.altair_chart(scatter_5d, use_container_width=True)

st.markdown("---")

# =============================
# SECTION 2: Long-Term Stock Impact (1Y)
# =============================

col3, col4 = st.columns([2, 1], gap="large")

with col3:
    scatter_1y = (
        alt.Chart(layoff_vs_immediate_df)
        .mark_circle(size=80, opacity=0.7, color="#10B981")
        .encode(
            x=alt.X("% Laid Off", title="% Workforce Laid Off"),
            y=alt.Y("% Change 1Y", title="% Change in Stock (1Y)"),
            tooltip=cols
        )
        .properties(width=550, height=400)
    )
    st.altair_chart(scatter_1y, use_container_width=True)

with col4:
    st.markdown("""
    ## Top Layoff Events vs. Long-Term Stock Impact
    **Description**  
    This chart shows the **percentage of workforce laid off** (`% Laid Off`)  
    against the **stock price change over one year** (`% Change 1Y`).  
    - Highlights how markets digest layoffs over the long run.  
    - Do large layoffs lead to *sustained recovery* or *continued decline*?
    """)

st.markdown("---")

# =============================
# Raw data display
# =============================
st.subheader("📊 Raw Data")
st.dataframe(layoff_vs_immediate_df, use_container_width=True)
