import yfinance as yf

data = yf.download(tickers="AAPL", period="5d", interval="1m")
print(data)
