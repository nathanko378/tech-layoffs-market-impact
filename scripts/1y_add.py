import pandas as pd
from fetch_1y_stock_data import price_change_1y, percent_change_1y

layoff_df_v2 = pd.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate.csv", usecols=["Company", "# Laid Off", "% Laid Off", "Date Added", "Ticker", "$ Change 5D", "% Change 5D"], na_filter=False)

#stores new columns in a list
longterm_list_dollar = []
longterm_list_percent = []

#creates each individual item in both columns
for index, row in layoff_df_v2.iterrows():
    longterm_list_dollar.append(price_change_1y(row[4], row[3]))
    longterm_list_percent.append(percent_change_1y(row[4], row[3]))

#assigns lists of items to columns
layoff_df_v2["$ Change 1Y"] = longterm_list_dollar
layoff_df_v2["% Change 1Y"] = longterm_list_percent

layoff_df_v2.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/layoff_vs_immediate_updated.csv")


