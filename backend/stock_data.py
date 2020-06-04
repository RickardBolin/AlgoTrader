import yfinance as yf
import time
from datetime import datetime

def get_stock_data(tickers, start=None, end=None, period="max", interval="1d", group_by='column', auto_adjust=False, prepost=False, threads=True,proxy=None):

	if interval[-1] == "m" and start == None:
		# Might be able to get about one more days worth of data somehow
		start = time.time() - 60*60*24*6
		start = datetime.utcfromtimestamp(start).strftime("%Y-%m-%d")
	"""
	Fetches the stock data (can be multiple at once) with prescribed options like start time etc.
	:return: Stock data.
	"""
	return yf.download(tickers=tickers, start=start, end=end, period=period, interval=interval, group_by=group_by, auto_adjust=auto_adjust, prepost=prepost, threads=threads, proxy=proxy)

