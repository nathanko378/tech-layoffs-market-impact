import pandas as pd

#removes companies without a ticker
layoff_df = pd.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/top_100_layoffs_csv", keep_default_na=False, usecols=["Company", "# Laid Off", "%", "Date Added", "Ticker"])
layoff_df = layoff_df[layoff_df["Ticker"] != "N/A"]
layoff_df.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_data_csv")
