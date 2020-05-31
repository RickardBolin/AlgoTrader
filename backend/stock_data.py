import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def plot_stock(ticker, start=None, end=None, interval=None):
	data = get_stock_data(ticker, start=start, end=end, interval=interval)
	data.plot(kind='line', y="Close")
	plt.show()


def get_stock_data(tickers, start=None, end=None, period="1mo" ,interval="1d", group_by='column', auto_adjust=False, prepost=False,threads=True,proxy=None):
	return yf.download(tickers=tickers, start=start, end=end, period=period, interval=interval, group_by=group_by, auto_adjust=auto_adjust, prepost=prepost, threads=threads, proxy=proxy)

