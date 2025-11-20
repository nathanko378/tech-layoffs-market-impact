import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import statsmodels.api as sm  # NEW: for regressions

# ----------------------------
# Load & process data
# ----------------------------
@st.cache_data
def load_layoff_data(csv_path: str) -> pd.DataFrame:
    cols = [
        "# Laid Off",
        "% Laid Off",
        "Date Added",
        "Ticker",
        "$ Change 5D",
        "% Change 5D",
        "$ Change 1Y",
        "% Change 1Y",
    ]
    df = pd.read_csv(csv_path, usecols=cols)

    # Parse dates
    df["Date Added"] = pd.to_datetime(df["Date Added"])

    # Clean % Laid Off
    df["% Laid Off"] = (
        df["% Laid Off"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace("", np.nan)
        .astype(float)
    )

    # Clean % change columns (in case there are % signs)
    for col in ["% Change 5D", "% Change 1Y"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.strip()
            .replace("", np.nan)
            .astype(float)
        )

    return df


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    """
    Compute a weighted average, safely handling NaNs and zero total weights.
    """
    mask = (~values.isna()) & (~weights.isna())
    if mask.sum() == 0:
        return np.nan
    w = weights[mask]
    v = values[mask]
    if w.sum() == 0:
        return np.nan
    return float((v * w).sum() / w.sum())


def compute_regression_stats(df: pd.DataFrame, x_col: str, y_col: str):
    """
    Fit a simple OLS regression y ~ x.
    Returns (slope, p_value, r_squared, model) or None if not enough data.
    """
    valid = df[[x_col, y_col]].dropna()
    if len(valid) < 3:
        return None

    X = sm.add_constant(valid[x_col])
    y = valid[y_col]
    model = sm.OLS(y, X).fit()

    slope = model.params[x_col]
    p_value = model.pvalues[x_col]
    r_squared = model.rsquared

    return slope, p_value, r_squared, model


# ----------------------------
# Streamlit page setup
# ----------------------------
st.set_page_config(
    page_title="Tech Layoffs & Market Impact Dashboard",
    page_icon="📉",
    layout="wide",
)

CSV_PATH = "/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate_updated.csv"
layoff_df = load_layoff_data(CSV_PATH)

# simple benchmark constant (nominal, illustrative)
AVG_SP500_1Y = 10.0  # you can adjust this number

# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("Filters")

tickers = sorted(layoff_df["Ticker"].dropna().unique())
selected_tickers = st.sidebar.multiselect(
    "Filter by ticker",
    options=tickers,
    default=tickers,
)

min_date = layoff_df["Date Added"].min().date()
max_date = layoff_df["Date Added"].max().date()
date_range = st.sidebar.date_input(
    "Event date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

min_layoffs = st.sidebar.slider(
    "Minimum # of employees laid off",
    min_value=0,
    max_value=int(layoff_df["# Laid Off"].max()),
    value=0,
    step=50,
)

mask = (
    layoff_df["Ticker"].isin(selected_tickers)
    & (layoff_df["Date Added"].dt.date >= date_range[0])
    & (layoff_df["Date Added"].dt.date <= date_range[1])
    & (layoff_df["# Laid Off"] >= min_layoffs)
)
filtered_df = layoff_df[mask].copy()

st.sidebar.markdown(f"**Events shown:** {len(filtered_df)}")

# ----------------------------
# Title & intro
# ----------------------------
st.title("Tech Layoffs & Stock Impacts (2021–2025)")

st.markdown(
    """
Interactive dashboard exploring the relationship between major tech layoff events and stock performance  
over short-term (5-day) and medium-term (1-year) horizons.

**Data sources:** Layoffs.fyi and pre-processed price data (via Yahoo Finance / yfinance).  

**Made By:** Nathan Ko
"""
)

st.markdown("---")

# ----------------------------
# Key findings (simple + weighted stats)
# ----------------------------
st.subheader("🔍 Key Findings (Based on Current Filters)")

if filtered_df.empty:
    st.warning("No events match your current filters. Try adjusting them in the sidebar.")
else:
    # Simple averages
    avg_5d = filtered_df["% Change 5D"].mean()
    avg_1y = filtered_df["% Change 1Y"].mean()

    # Weighted by % Laid Off
    w_avg_5d = weighted_mean(filtered_df["% Change 5D"], filtered_df["% Laid Off"])
    w_avg_1y = weighted_mean(filtered_df["% Change 1Y"], filtered_df["% Laid Off"])

    # Correlation between layoff severity and returns (guard against too few points)
    if filtered_df[["% Laid Off", "% Change 5D"]].dropna().shape[0] >= 2:
        corr_5d = filtered_df[["% Laid Off", "% Change 5D"]].corr().iloc[0, 1]
    else:
        corr_5d = np.nan

    if filtered_df[["% Laid Off", "% Change 1Y"]].dropna().shape[0] >= 2:
        corr_1y = filtered_df[["% Laid Off", "% Change 1Y"]].corr().iloc[0, 1]
    else:
        corr_1y = np.nan

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg 1-year S&P 500 change (benchmark)", f"{AVG_SP500_1Y:.2f}%")
    c2.metric("Avg 5-day stock move (simple)", f"{avg_5d:.2f}%")
    c3.metric("Avg 1-year stock move (simple)", f"{avg_1y:.2f}%")

    d1, d2 = st.columns(2)
    d1.metric("Avg 5-day stock move (weighted by % laid off)", f"{w_avg_5d:.2f}%")
    d2.metric("Avg 1-year stock move (weighted by % laid off)", f"{w_avg_1y:.2f}%")

    st.markdown(
        f"""
- Correlation between **layoff size (% Laid Off)** and **5-day return**: `{corr_5d:.2f}`  
- Correlation between **layoff size (% Laid Off)** and **1-year return**: `{corr_1y:.2f}`  

More negative values suggest that **larger layoffs** tend to line up with **worse performance** over that horizon,  
while values near zero suggest a weak or no clear relationship.
"""
    )

st.markdown("---")

# ----------------------------
# Regression section
# ----------------------------
st.subheader("📈 Regression: Layoff % vs Stock Returns")

if filtered_df.empty:
    st.info("Not enough data for regression under current filters.")
else:
    reg_window = st.radio(
        "Choose return window for regression:",
        ("5-day return", "1-year return"),
        horizontal=True,
    )

    if reg_window == "5-day return":
        y_col = "% Change 5D"
        label = "5-day return (%)"
    else:
        y_col = "% Change 1Y"
        label = "1-year return (%)"

    reg_result = compute_regression_stats(filtered_df, "% Laid Off", y_col)

    if reg_result is None:
        st.info("Not enough non-missing data points to run regression.")
    else:
        slope, p_value, r_squared, model = reg_result

        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Slope (β)", f"{slope:.3f} % per 1% layoff")
        col_b.metric("R²", f"{r_squared:.3f}")
        col_c.metric("p-value (β)", f"{p_value:.4f}")
        col_d.metric(
            "Sample size (N)",
            f"{len(filtered_df[['% Laid Off', y_col]].dropna())}",
        )

        st.caption(
            f"""
Model: `{label} = α + β × (% Laid Off) + ε`  
A **negative β** suggests larger layoffs are associated with more negative {reg_window}.
"""
        )

        with st.expander("Show full regression summary"):
            st.text(model.summary().as_text())

st.markdown("---")

# ----------------------------
# Immediate stock impact (short-term)
# ----------------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown(
        """
### Top Layoff Events vs Immediate Stock Impact

This scatter plot compares:

- **% of workforce laid off** (`% Laid Off`)  
- **5-day stock price change** (`% Change 5D`)  

Each point is a layoff event.  

The regression line gives a sense of the **overall relationship** between layoff severity and the short-term market reaction.
"""
    )

with col2:
    if filtered_df.empty:
        st.info("No data to display for the current filters.")
    else:
        base_5d = (
            alt.Chart(filtered_df)
            .mark_circle(size=70, opacity=0.7)
            .encode(
                x=alt.X("% Laid Off", title="% Workforce Laid Off"),
                y=alt.Y("% Change 5D", title="% Change in Stock (5D, %)"),
                color=alt.Color("Ticker:N", legend=None),
                tooltip=[
                    "Ticker",
                    "Date Added",
                    "# Laid Off",
                    "% Laid Off",
                    "% Change 5D",
                ],
            )
            .properties(height=400)
        )

        reg_line_5d = base_5d.transform_regression(
            "% Laid Off", "% Change 5D", method="linear"
        ).mark_line(color="black")

        st.altair_chart(base_5d + reg_line_5d, use_container_width=True)

st.markdown("---")

# ----------------------------
# Long-term stock impact (medium-term)
# ----------------------------
col3, col4 = st.columns([2, 1], gap="large")

with col3:
    if filtered_df.empty:
        st.info("No data to display for the current filters.")
    else:
        base_1y = (
            alt.Chart(filtered_df)
            .mark_circle(size=70, opacity=0.7)
            .encode(
                x=alt.X("% Laid Off", title="% Workforce Laid Off"),
                y=alt.Y("% Change 1Y", title="% Change in Stock (1Y, %)"),
                color=alt.Color("Ticker:N", legend=None),
                tooltip=[
                    "Ticker",
                    "Date Added",
                    "# Laid Off",
                    "% Laid Off",
                    "% Change 1Y",
                ],
            )
            .properties(height=400)
        )

        reg_line_1y = base_1y.transform_regression(
            "% Laid Off", "% Change 1Y", method="linear"
        ).mark_line(color="black")

        st.altair_chart(base_1y + reg_line_1y, use_container_width=True)

with col4:
    st.markdown(
        """
### Top Layoff Events vs Medium-Term Stock Impact

This scatter plot compares:

- **% of workforce laid off** (`% Laid Off`)  
- **1-year stock price change** (`% Change 1Y`)  

Each point is a layoff event.  

The regression line shows whether **larger layoffs** are associated with **better or worse performance** over the 1-year horizon.
"""
    )

st.markdown("---")

# ----------------------------
# Correlation: Layoff Severity vs Performance
# ----------------------------
st.subheader("📊 Correlation Matrix: Layoff Severity vs Performance")

if not filtered_df.empty:
    possible_corr_cols = [
        "% Laid Off",
        "# Laid Off",
        "% Change 5D",
        "% Change 1Y",
    ]
    corr_cols = [c for c in possible_corr_cols if c in filtered_df.columns]

    if len(corr_cols) < 2:
        st.info("Not enough numeric columns available to compute correlations.")
    else:
        corr_df = filtered_df[corr_cols].corr(min_periods=3)

        if corr_df.isna().all().all():
            st.info(
                "Not enough overlapping data to compute meaningful correlations. "
                "Try widening your filters."
            )
        else:
            corr_melt = corr_df.reset_index().melt("index")
            corr_melt.columns = ["Variable 1", "Variable 2", "Correlation"]

            heatmap = (
                alt.Chart(corr_melt)
                .mark_rect()
                .encode(
                    x=alt.X("Variable 1:O", sort=None),
                    y=alt.Y("Variable 2:O", sort=None),
                    color=alt.Color(
                        "Correlation:Q",
                        scale=alt.Scale(scheme="redblue", domain=(-1, 1)),
                    ),
                    tooltip=[
                        "Variable 1",
                        "Variable 2",
                        alt.Tooltip("Correlation:Q", format=".2f"),
                    ],
                )
                .properties(height=350)
            )

            text = heatmap.mark_text(baseline="middle").encode(
                text=alt.Text("Correlation:Q", format=".2f")
            )

            st.altair_chart(heatmap + text, use_container_width=True)

            st.markdown(
                """
Key relationships of interest:

- **`% Laid Off` vs `% Change 5D`** – short-term reaction to layoff size  
- **`% Laid Off` vs `% Change 1Y`** – medium-term reaction to layoff size  

Negative correlations suggest that **bigger layoffs** line up with **worse performance**.
"""
            )
else:
    st.info("No data available for correlation with the current filters.")

st.markdown("---")

# ----------------------------
# Raw data
# ----------------------------
st.subheader("📊 Raw Layoff Event Data")

if filtered_df.empty:
    st.info("No rows to display for the current filters.")
else:
    display_cols = [
        "Date Added",
        "Ticker",
        "# Laid Off",
        "% Laid Off",
        "% Change 5D",
        "% Change 1Y",
        "$ Change 5D",
        "$ Change 1Y",
    ]
    st.dataframe(
        filtered_df[display_cols].sort_values("Date Added", ascending=False),
        use_container_width=True,
    )

# ----------------------------
# Methodology
# ----------------------------
st.subheader("🧠 Methodology & Project Notes")

st.markdown(
    """
- Collected **tech layoff events** (company, date, # laid off, % of workforce).  
- Merged each event with **stock performance** over **5 days** and **1 year** after the announcement.  
- Cleaned and transformed the data in Python (pandas).  
- Built an **interactive dashboard** in **Streamlit** with:
  - Filters for ticker, date, and layoff size  
  - Visualizations of layoff severity vs stock performance  
  - Correlation, weighted-average, and regression analysis between layoff size and returns  

The goal of this project is to challenge the assumption that layoffs are automatically “good for shareholders” by  
**looking directly at how markets have actually reacted to these events over time.**
"""
)
