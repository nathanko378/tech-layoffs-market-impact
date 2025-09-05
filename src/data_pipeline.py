import yfinance as yf
import pandas as pd

ticker = "GOOG"
date = "2025-06-05"
date2 = "2025-06-10"

start = pd.to_datetime(date)
end = start + pd.Timedelta(days=1)  # need at least one day after

start2 = pd.to_datetime(date2)
end2 = start2 + pd.Timedelta(days=1)

data = yf.download(ticker, start=start, end=end)
data2 = yf.download(ticker, start=start2, end=end2)

print(data["Close"], data2["Close"])
print((180-169)/169)