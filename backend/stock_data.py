import yfinance as yf


def get_stock_data(tickers, start=None, end=None, period="1mo", interval="1d", group_by='column', auto_adjust=False, prepost=False, threads=True,proxy=None):
	"""
	Fetches the stock data (can be multiple at once) with prescribed options like start time etc.
	:return: Stock data.
	"""
	return yf.download(tickers=tickers, start=start, end=end, period=period, interval=interval, group_by=group_by, auto_adjust=auto_adjust, prepost=prepost, threads=threads, proxy=proxy)

