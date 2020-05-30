import sys
import csv
sys.path.append("..")

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from backend import stock_data as sd
from collections import namedtuple
from tkfilterlist import FilterList


class StockWindow:

    def __init__(self, StockTab):
        self.StockTab = StockTab
        self.StockPlot = StockPlot(StockTab, self)
        self.StockList = StockList(StockTab, self.StockPlot)


class StockPlot:

    def __init__(self, root, StockWindow):
        self.StockWindow = StockWindow
        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack(side="left", anchor=tk.NW)

        # Initialize stock window with Apple stock data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        stock_data = sd.get_stock_data("AAPL", start="2013-05-25", interval="1d")
        self.a = self.figure.add_subplot(111)
        self.graph = self.a.plot(stock_data["Close"])
        self.canvas = FigureCanvasTkAgg(self.figure, self.stock_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_stock(self, ticker):
        stock_data = sd.get_stock_data(ticker, start="2013-05-25", interval="1d")
        x = stock_data["Close"]
        print(x.keys())
        dates = x.keys()
        prices = x.get("Close")
        print(dates)
        print(prices)
        self.graph[0].set_data(dates[1:], prices[1:])
        print(self.graph[0])

        #self.a.set_ylim([0.9*min(stock_data["Close"]), 1.1*max(stock_data["Close"])])
        self.canvas.draw()


class StockList:

    def __init__(self, root, StockPlot):
        self.StockPlot = StockPlot
        self.root = root
        self.stock_list_frame = tk.Frame(self.root)
        self.stock_list_frame.pack(anchor=tk.NE)
        stock_names = self.load_ticker_name_info("NASDAQ")
        self.stock_list = FilterList(self.stock_list_frame,
                height=27,
                source=stock_names,
                display_rule=lambda item: item[0] + ": " + item[1],
                filter_rule=lambda item, text:
                            item[0].lower().startswith(text.lower()) or item[1].lower().startswith(text.lower()))
        
        self.stock_list.pack(side="top", expand=1, fill="both")
        self.stock_list.bind('<Return>', self.search)

    def search(self, event):
        ticker = self.stock_list.selection()[0]
        self.StockPlot.update_stock(ticker)


    @staticmethod
    def load_ticker_name_info(exchange):
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info


