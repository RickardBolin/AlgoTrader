import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def plot_stock(symbols, start, end=None, interval=None):
	data = yf.download(tickers=symbols, start=start, end=end, interval=interval)
	data.plot(kind='line', y="High")
	plt.show()
