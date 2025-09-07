import pandas as pd
from fetch_immediate_stock_data import price_change_5d, percent_change_5d

#Format: #company_ticker, num_layoffs, percent_layoffs, dollar_change_stock_value, percent_change_stock_value

layoff_vs_immediate = pd.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_data_csv", usecols=["Company", "# Laid Off", "%", "Date Added", "Ticker"])
immediate_list_dollar = []
for index, row in layoff_vs_immediate.iterrows():
    immediate_list_dollar.append(price_change_5d(row[4], row[3]))
    print(immediate_list_dollar)
