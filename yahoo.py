import yfinance as yf

tickers = yf.Tickers('msft aapl goog')
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
tickers.msft.info
tickers.aapl.history(period="1mo")
tickers.goog.actions
