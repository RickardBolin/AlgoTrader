import yfinance as yf
import pandas as pd
import matplotlib as plt

def plot_stock(symbols, start, end=None):
	data = yf.download(tickers=symbols, start=start, end=end)
	data.plot(kind='line',x=data["Date"], y= data["High"])
