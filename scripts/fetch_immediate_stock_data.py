import yfinance as yf
import pandas as pd

def price_change_5d(ticker, start_dt):
    #set start and end date
    start_dt = pd.to_datetime(start_dt)
    end_dt_exclusive = start_dt + pd.Timedelta(days=6)
    end_dt = start_dt + pd.Timedelta(days=5)
    stock = yf.download(ticker, start=start_dt, end=end_dt_exclusive)
    stock.reset_index(inplace=True)

    #find start and end value with start and end date
    start_value = stock[stock["Date"] == start_dt].Close.iloc[0]
    end_value = stock[stock["Date"] == end_dt].Close.iloc[0]

    #calculate change
    change = round(end_value - start_value, 2)
    return change

def percent_change_5d(ticker, start_dt):
    start_dt = pd.to_datetime(start_dt)
    end_dt_exclusive = start_dt + pd.Timedelta(days=6)
    end_dt = start_dt + pd.Timedelta(days=5)
    stock = yf.download(ticker, start=start_dt, end=end_dt_exclusive)
    stock.reset_index(inplace=True)

    # find start and end value with start and end date
    start_value = stock[stock["Date"] == start_dt].Close.iloc[0]
    end_value = stock[stock["Date"] == end_dt].Close.iloc[0]

    # calculate change in percent
    change = round((end_value - start_value)/start_value * 100, 2)
    return change


print(percent_change_5d("goog", "6/5/2025")) #example
