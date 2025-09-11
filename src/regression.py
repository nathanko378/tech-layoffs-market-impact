import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("/data/processed/d2", usecols=["# Laid Off", "%", "Date Added", "Ticker", "$ Change 5D", "% Change 5D"])
print(df)