import pandas

#Format: #company_ticker, num_layoffs, percent_layoffs, dollar_change_stock_value, percent_change_stock_value

ticker_and_layoff_num_df = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/ticker_and_layoff_num")
ticker_and_layoff_percent_df = pandas.read_csv("/Users/nathanko/PycharmProjects/tech-layoffs-stock-analysis/data/processed/ticker_and_layoff_percent")

for stock in ticker_and_layoff_percent_df["Ticker"]:
    print(stock, fetch_percent_change(stock))
