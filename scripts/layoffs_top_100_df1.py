import pandas
import requests
import yfinance as yf

#reads csv selecting columns Company, # Laid Off, %, and Date Added
desired_columns = ["Company", "# Laid Off", "%", "Date Added"]
layoff_data = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/Layoffs.fyi  - Tech Layoffs Tracker.csv", usecols=desired_columns)
print(layoff_data.head)

#top 50 companies in # employees layed off
top_100_layed_off = layoff_data.sort_values(by="# Laid Off", ascending=False).head(100)

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

#tickers of top 50 companies
###top_50_ticker = [get_ticker(company) for company in top_100_layed_off.Company]

#replaces company column with ticker to top 100 dataframe
###top_100_layed_off["Ticker"] = top_100_layed_off["Company"].apply(get_ticker)

#creating csv to save data
###top_100_layed_off.to_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/raw/top_100_layoffs_csv")





