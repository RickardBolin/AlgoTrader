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
        self.Buttons = Buttons(StockTab)


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


class Buttons:

    def __init__(self, root):
        self.root = root
        self.button_frame = tk.Frame(self.root, width=30, height=10)
        self.button_frame.pack(anchor=tk.SE)

        self.stock_entry = tk.Entry(self.button_frame)
        self.stock_entry.grid(row=0, column=1)

        self.search_button = tk.Button(self.button_frame, text="Search")
        self.search_button.grid(row=0)
        self.search_button.bind("<Button-1>", self.search_stock)

    def search_stock(self, event):
        stock = self.stock_entry.get()
        StockPlot.update_stock(stock)


class StockList:

    def __init__(self, root):
        self.root = root
        self.stock_list_frame = tk.Frame(self.root)
        self.stock_list_frame.pack(anchor=tk.NE)
        '''
        self.stock_list = tk.Listbox(self.stock_list_frame, width=27, height=27)
        self.stock_list.pack(side="left")

        self.stock_scroller = tk.Scrollbar(self.stock_list_frame, orient="vertical")
        self.stock_scroller.config(command=self.stock_list.yview)
        self.stock_scroller.pack(side="right", fill="y")

        self.stock_list.config(yscrollcommand=self.stock_scroller.set)
        '''
        stock_names = self.load_ticker_name_info("NASDAQ")
        self.stock_list = FilterList(self.stock_list_frame,
                source=stock_names,
                display_rule=lambda item: item[0],
                filter_rule=lambda item, text:
                            item[0].lower().startswith(text.lower()))
        
        self.stock_list.pack(side="top", expand=1, fill="both")

#        for i, stock_name in enumerate(stock_names):
#            self.stock_list.insert(i, stock_name.ticker + ": " + stock_name.name)

    @staticmethod
    def load_ticker_name_info(exchange):
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info


