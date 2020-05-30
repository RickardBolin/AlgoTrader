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
from datetime import datetime


class StockWindow:
    """
    POTENTIALLY UNFINISHED
    Class for the entire stock tab.
    Currently contains its tab, a stockplot and the list of stocks in an exchange.
    """

    def __init__(self, stock_tab):
        self.StockTab = stock_tab
        self.StockPlot = StockPlot(stock_tab)
        self.StockList = StockList(stock_tab, self.StockPlot)


class StockPlot:
    """
    POTENTIALLY UNFINISHED
    Class which handles the stockplot.
    """

    def __init__(self, root):
        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack(side="left", anchor=tk.NW)

        # Initialize stock window with Apple stock data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        stock_data = sd.get_stock_data("AAPL", start="2016-05-25", interval="1d")
        self.a = self.figure.add_subplot(111)
        self.graph_list = self.a.plot(stock_data["Close"], label="AAPL")
        self.a.legend()
        self.canvas = FigureCanvasTkAgg(self.figure, self.stock_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_stock_plot(self, tickers):
        """
        UNFINISHED
        Updates the stock plot to the specified ticker.
        Shall also be expanded to allow specifications of dates, interval etc.
        :param ticker: Stock ticker of stock to be plotted.
        """

        # We remove all line and plot new ones according to the tickers, might want to change this to be more efficient!
        self.graph_list = []
        y_max = 0
        y_min = 1e30
        # x_max = 0
        # x_min = 1e30
        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start="2016-05-25", interval="1d")
            self.graph_list.append(self.a.plot(stock_data["Close"], label=ticker))
            y_max = max(y_max, max(stock_data["Close"]))
            y_min = min(y_min, min(stock_data["Close"]))
            # x_max = max(x_max, datetime.strptime(str(stock_data.index[-1]), "%Y-%m-%d %H:%M:%S-%?:%?"))
            # x_min = min(x_min, datetime.strptime(str(stock_data.index[0]), "%Y-%m-%d %H:%M:%S-%?:%?"))

        self.a.legend()
        self.a.set_ylim([0.9 * y_min, 1.1 * y_max])
        # self.a.set_xlim([x_min, x_max])
        self.canvas.draw()


class StockList:
    """
    NB! SEVERAL FEATURES IN THIS CLASS ARE SUBJECT TO CHANGE.
    Class for the filterable stocklist.
    Contains its rootframe and the stock plot which shall be updated.
    """

    def __init__(self, root, stock_plot):
        self.stock_plot = stock_plot
        self.root = root

        self.stock_list_frame = tk.Frame(self.root)
        self.stock_list_frame.pack(anchor=tk.NE)
        stock_names = self.load_ticker_name_info("NASDAQ")
        self.stock_list = FilterList(self.stock_list_frame,
                                     height=27,
                                     source=stock_names,
                                     display_rule=lambda item: item[0] + ": " + item[1],
                                     filter_rule=lambda item, text:
                                     item[0].lower().startswith(text.lower()) or item[1].lower().startswith(
                                         text.lower()))

        self.stock_list.pack(side="top", expand=1, fill="both")
        self.stock_list.bind('<Return>', self.search)
        self.stock_list.bind('<Double-Button-1>', self.search)
        self.stock_list.focus_set()

    def search(self, event):
        """
        SKALL ÄNDRAS TILL ATT UPPDATERA WORKSPACE!!!!!!!!!!!!
        Finds the
        """
        tickers = [self.stock_list.selection()[0]]
        self.stock_plot.update_stock_plot(tickers)

    @staticmethod
    def load_ticker_name_info(exchange):
        """
        Fetches stock ticker and company name from an exchange and returns them as a list of namedtuples.
        :param exchange: Choice of stock exchange.
        :return: List of namedtuples with stock ticker and company name from stock exchange.
        """
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info
