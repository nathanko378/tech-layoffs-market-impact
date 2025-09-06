import pandas
import requests

#quicker access to cleaning_stock_data_1
layoff_data_v2_num = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/top_100_layoffs_csv", keep_default_na=False, usecols=["Ticker", "# Laid Off"])
layoff_data_v2_percent = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/top_100_layoffs_csv", keep_default_na=False, usecols=["Ticker", "%"])

#removes companies with tickers as N/A
top_with_ticker_num = layoff_data_v2_num[layoff_data_v2_num["Ticker"] != "N/A"]
top_with_ticker_percent = layoff_data_v2_percent[layoff_data_v2_percent["Ticker"] != "N/A"]

#remove duplicates and sort by lowest to greatest, selecting top 50 only
final_df_layoff_num = top_with_ticker_num.loc[top_with_ticker_num.groupby("Ticker")["# Laid Off"].idxmax()].sort_values(by="# Laid Off", ascending=False)
final_df_layoff_percent = top_with_ticker_percent.loc[top_with_ticker_percent.groupby("Ticker")["%"].idxmax()].sort_values(by="%", ascending=False)

#final_df_layoff_num.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/ticker_and_layoff_num")
#final_df_layoff_percent.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/ticker_and_layoff_percent")