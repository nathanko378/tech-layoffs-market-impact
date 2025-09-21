import yfinance as yf
import pandas as pd

def price_change_5d(ticker, start_dt):
    start_dt = pd.to_datetime(start_dt)
    end_dt = start_dt + pd.Timedelta(days=5)

    stock = yf.download(
        ticker,
        start=start_dt - pd.Timedelta(days=2),
        end=end_dt + pd.Timedelta(days=2)
    )
    if stock.empty:
        raise ValueError("No stock data returned for given period.")

    stock.reset_index(inplace=True)

    #find closest trading day to start_dt and end_dt
    start_idx = (stock["Date"] - start_dt).abs().idxmin()
    end_idx = (stock["Date"] - end_dt).abs().idxmin()

    #returns a series if there are duplicates
    start_value = float(stock.loc[start_idx, "Close"])
    end_value = float(stock.loc[end_idx, "Close"])

    return round(end_value - start_value, 2)

def percent_change_5d(ticker, start_dt):
    start_dt = pd.to_datetime(start_dt)
    end_dt = start_dt + pd.Timedelta(days=5)

    stock = yf.download(
        ticker,
        start=start_dt - pd.Timedelta(days=2),
        end=end_dt + pd.Timedelta(days=2)
    )
    if stock.empty:
        raise ValueError("No stock data returned for given period.")

    stock.reset_index(inplace=True)

    #find closest trading day to start_dt and end_dt
    start_idx = (stock["Date"] - start_dt).abs().idxmin()
    end_idx = (stock["Date"] - end_dt).abs().idxmin()

    #returns a series if there are duplicates
    start_value = float(stock.loc[start_idx, "Close"])
    end_value = float(stock.loc[end_idx, "Close"])

    return round((end_value - start_value)/start_value*100, 2)



