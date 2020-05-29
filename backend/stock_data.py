import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def plot_stock(ticker, start, end=None, interval=None):
	data = get_stock_data(ticker, start=start, end=end, interval=interval)
	data.plot(kind='line', y="Close")
	plt.show()


def get_stock_data(ticker, start, end=None, interval=None):
	return yf.download(tickers=ticker, start=start, end=end, interval=interval)

