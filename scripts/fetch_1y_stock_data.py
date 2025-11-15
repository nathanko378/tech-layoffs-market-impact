import yfinance as yf
import pandas as pd
from datetime import datetime

def price_change_1y(ticker, start_dt):
    start_dt = pd.to_datetime(start_dt)
    today = pd.Timestamp.today().normalize()
    end_dt = min(start_dt + pd.Timedelta(days=365), today)  # cap at today

    #download a buffer around both ends to handle non-trading days
    stock = yf.download(
        ticker,
        start=start_dt - pd.Timedelta(days=2),
        end=end_dt + pd.Timedelta(days=2)
    )
    if stock.empty:
        raise ValueError(f"No stock data returned for {ticker} in this period.")

    stock.reset_index(inplace=True)

    #find closest trading days
    start_idx = (stock["Date"] - start_dt).abs().idxmin()
    end_idx = (stock["Date"] - end_dt).abs().idxmin()

    start_value = float(stock.loc[start_idx, "Close"])
    end_value = float(stock.loc[end_idx, "Close"])

    return round(end_value - start_value, 2)

def percent_change_1y(ticker, start_dt):
    start_dt = pd.to_datetime(start_dt)
    today = pd.Timestamp.today().normalize()
    end_dt = min(start_dt + pd.Timedelta(days=365), today)

    stock = yf.download(
        ticker,
        start=start_dt - pd.Timedelta(days=2),
        end=end_dt + pd.Timedelta(days=2)
    )
    if stock.empty:
        raise ValueError(f"No stock data returned for {ticker} in this period.")

    stock.reset_index(inplace=True)

    start_idx = (stock["Date"] - start_dt).abs().idxmin()
    end_idx = (stock["Date"] - end_dt).abs().idxmin()

    start_value = float(stock.loc[start_idx, "Close"])
    end_value = float(stock.loc[end_idx, "Close"])

    return round((end_value - start_value) / start_value * 100, 2)

#example usage:
print(price_change_1y("AAPL", "2025-09-30"))
print(percent_change_1y("AAPL", "2025-09-30"))
