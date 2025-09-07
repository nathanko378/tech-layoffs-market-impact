import pandas as pd
from fetch_immediate_stock_data import price_change_5d, percent_change_5d

#Format: #company_ticker, num_layoffs, percent_layoffs, dollar_change_stock_value, percent_change_stock_value

layoff_vs_immediate = pd.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_data_csv", usecols=["Company", "# Laid Off", "%", "Date Added", "Ticker"])
immediate_list_dollar = []
immediate_list_percent = []

for index, row in layoff_vs_immediate.iterrows():
    immediate_list_dollar.append(price_change_5d(row[4], row[3]))
    immediate_list_percent.append(percent_change_5d(row[4], row[3]))

layoff_vs_immediate["$ Change 5D"] = immediate_list_dollar
layoff_vs_immediate["% Change 5D"] = immediate_list_percent

layoff_vs_immediate.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoffs_stock_5day_change.csv")