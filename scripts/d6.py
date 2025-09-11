import pandas as pd

layoff_df = pd.read_csv("/data/raw/d4", keep_default_na=False, usecols=["Company", "# Laid Off", "%", "Date Added", "Ticker"])
layoff_df = layoff_df[layoff_df["Ticker"] != "N/A"]
layoff_df.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/d1")