import pandas
import requests
import yfinance as yf

#reads csv selecting columns Company, # Laid Off, %, Date Added, and Stage
desired_columns = ["Company", "# Laid Off", "%", "Date Added", "Stage"]
layoff_data = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/Layoffs.fyi  - Tech Layoffs Tracker.csv", usecols=desired_columns)

#sorts by # Laid Off, and only selects companies Post-IPO
layoff_data = layoff_data.sort_values(by="# Laid Off", ascending=False)
layoff_data = layoff_data[layoff_data["Stage"] == "Post-IPO"]
print(layoff_data)

#functions to convert company name to company ticker
def get_ticker(company_name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    try:
        res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
        data = res.json()

        # Check if 'quotes' exists and has at least one result
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0].get('symbol', "N/A")
        else:
            return "N/A"
    except Exception:
        return "N/A"

#adds column "Ticker", removing invalid tickers
layoff_data["Ticker"] = layoff_data["Company"].apply(get_ticker)
layoff_data = layoff_data[layoff_data["Ticker"] != "N/A"]

#to new csv
layoff_data.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/clean_layoff_data.csv")
