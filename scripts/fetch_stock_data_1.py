import yfinance as yf
import pandas as pd

#company_ticker, num_layoffs, percent_layoffs, dollar_change_stock_value, percent_change_stock_value

#fetch dollar change of stock from start of 2025 to present
def fetch_dollar_change(ticker, start="2025-01-01"):
    stock = yf.download(ticker, start=start)
    stock.reset_index(inplace=True)

    day_1_close = (round(float(stock.iloc[0].Close), 2))
    present_close = (round(float(stock.iloc[len(stock)-1].Close), 2))

    dollar_change_stock_value = round(present_close-day_1_close, 2)
    return dollar_change_stock_value

#fetch percent change of stock from start of 2025 to present
def fetch_percent_change(ticker, start="2025-01-01"):
    stock = yf.download(ticker, start=start)
    stock.reset_index(inplace=True)

    day_1_close = (round(float(stock.iloc[0].Close), 2))
    present_close = (round(float(stock.iloc[len(stock)-1].Close), 2))

    percent_change_stock_value = round(round(present_close - day_1_close, 2)/day_1_close * 100, 2)
    return percent_change_stock_value

print(fetch_dollar_change("goog"), fetch_percent_change("goog")) #example