import pandas as pd
from fetch_immediate_stock_data import price_change_5d, percent_change_5d

#Format: #company_ticker, num_layoffs, percent_layoffs, dollar_change_stock_value, percent_change_stock_value

#final data cleaning, removing companies with null %, and other invalid tickers
layoff_df = pd.read_csv("/data/raw/clean_layoff_data.csv", usecols=["Company", "# Laid Off", "%", "Date Added", "Ticker"], na_filter=False).head(554)
#layoff_df = layoff_df[layoff_df["Ticker"] != "N/A"]
layoff_df = layoff_df[layoff_df["%"] != ""]
layoff_df = layoff_df[layoff_df["Ticker"].str.match(r'^[A-Za-z]+$')]

#stores new columns in a list
immediate_list_dollar = []
immediate_list_percent = []

#creates each individual item in both columns
for index, row in layoff_df.iterrows():
    immediate_list_dollar.append(price_change_5d(row[4], row[3]))
    immediate_list_percent.append(percent_change_5d(row[4], row[3]))

#assigns lists of items to columns
layoff_df["$ Change 5D"] = immediate_list_dollar
layoff_df["% Change 5D"] = immediate_list_percent

layoff_df.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate.csv")