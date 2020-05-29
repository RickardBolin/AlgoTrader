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
        self.StockWindow = StockPlot(StockTab)
        self.StockList = StockList(StockTab)


class StockPlot:

    def __init__(self, root):

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

    def update_stock(self, stock):
        stock_data = sd.get_stock_data(stock, start="2019-05-25", interval="1d")
        self.graph[0].set_ydata(stock_data["Close"])
        self.a.set_ylim([0.9*min(stock_data["Close"]), 1.1*max(stock_data["Close"])])
        self.canvas.draw()


class StockList:

    def __init__(self, root):
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

    @staticmethod
    def load_ticker_name_info(exchange):
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info


