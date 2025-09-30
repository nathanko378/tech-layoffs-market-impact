import yfinance as yf
import pandas as pd

stock = yf.Ticker('VG')
hist = stock.history(period="1y")

print(hist.head())

import matplotlib.pyplot as plt

# 50 day moving average
hist['SMA_50'] = hist['Close'].rolling(window=50).mean()


plt.figure(figsize=(12, 6))
plt.plot(hist['Close'], label='Close Price')
plt.plot(hist['SMA_50'], label='50-Day SMA')
plt.legend()
plt.show()

