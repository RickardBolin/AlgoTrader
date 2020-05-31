import sys
import csv

sys.path.append("..")

import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
import pandas as pd

register_matplotlib_converters()
from backend import stock_data as sd
from collections import namedtuple
from tkfilterlist import FilterList


class StockWindow:
    """
    POTENTIALLY UNFINISHED
    Class for the entire stock tab.
    Currently contains its tab, a stockplot and the list of stocks in an exchange.
    """

    def __init__(self, stock_tab):
        self.stock_tab = stock_tab
        self.stock_plot = StockPlot(self.stock_tab)
        self.stock_list = StockList(self.stock_tab)


class StockPlot:
    """
    POTENTIALLY UNFINISHED
    Class which handles the stockplot.
    """

    def __init__(self, root):
        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.stock_frame)
        self.button_frame.pack(side="bottom", anchor=tk.SE)
        self.stock_frame.pack(side="left", anchor=tk.SW)

        # Add empty stock figure
        self.plot_time_frame = "3 Years"
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.stock_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.stock_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add buttons to change viewing dates
        times = ["one_min", "one_day", "one_month", "one_year", "three_years"]
        self.buttons = []
        for i, time in enumerate(times):
            self.buttons.append(tk.Button(self.button_frame, text=time))
            self.buttons[i].grid(row=0, column=i)
            self.buttons[i].bind("<Button-1>", eval("self." + time + "_button"))

        self.PLOT_OPTIONS = [
            'Regular',
            'Percentual change',
            'Growth since time t0'
        ]
        self.plot_style = tk.StringVar(self.stock_frame)
        self.plot_style.set(self.PLOT_OPTIONS[0])

        self.plot_menu = tk.OptionMenu(self.stock_frame, self.plot_style, *self.PLOT_OPTIONS)
        self.plot_menu.pack(anchor=tk.NW)

    def update_stock_plot(self, tickers):
        """
        UNFINISHED
        Updates the stock plot to the specified tickers.
        Shall also be expanded to allow specifications of dates, interval etc.
        :param tickers: Stock tickers of stock to be plotted.
        """

        # We remove all lines and plot new ones according to the tickers, might want to change this to be more efficient!
        self.figure.clear()
        self.a = self.figure.add_subplot(111)

        y_max = 0
        y_min = 1e30

        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start="2016-05-25", interval="1d")
            self.a.plot(stock_data["Close"], label=ticker)
            y_max = max(y_max, max(stock_data["Close"]))
            y_min = min(y_min, min(stock_data["Close"]))

        self.a.legend()
        self.a.set_ylim([0.9 * y_min, 1.1 * y_max])
        self.a.set_ylabel('$')
        self.a.set_xlabel('Date')
        self.canvas.draw()

    def percentual_change_plot(self, tickers):
        self.figure.clear()
        self.a = self.figure.add_subplot(111)

        y_max = 0
        y_min = 1e30

        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start="2016-05-25", interval="1d")
            closed_values = stock_data['Close']
            one_day_ahead_closed_values = closed_values.shift(1)
            percentual_change = 100*(one_day_ahead_closed_values - closed_values).div(closed_values)
            percentual_change = percentual_change.dropna()
            self.a.plot(percentual_change, label=ticker)
            y_max = max(y_max, max(percentual_change))
            y_min = min(y_min, min(percentual_change))

        self.a.legend()
        self.a.set_ylim([0.9 * y_min, 1.1 * y_max])
        self.a.set_ylabel('%')
        self.a.set_xlabel('Date')
        self.canvas.draw()


    # Hur slår vi ihop detta till en funktion?!
    def one_min_button(self, event):
        self.plot_time_frame = "1 min"

    def one_day_button(self, event):
        self.plot_time_frame = "1 day"

    def one_month_button(self, event):
        self.plot_time_frame = "1 month"

    def one_year_button(self, event):
        self.plot_time_frame = "1 Year"

    def three_years_button(self, event):
        self.plot_time_frame = "3 Years"



class StockList:
    """
    NB! SEVERAL FEATURES IN THIS CLASS ARE SUBJECT TO CHANGE.
    Class for the filterable stocklist.
    Contains its rootframe and the stock plot which shall be updated.
    """

    def __init__(self, root):
        self.root = root

        self.stock_list_frame = tk.LabelFrame(self.root, text='Stocks')
        self.stock_list_frame.pack(side="right", anchor=tk.NE, fill="y")
        stock_names = self.load_ticker_name_info("NASDAQ")
        self.stock_list = FilterList(self.stock_list_frame,
                                     height=27,
                                     source=stock_names,
                                     display_rule=lambda item: item[0] + ": " + item[1],
                                     filter_rule=lambda item, text:
                                     item[0].lower().startswith(text.lower()) or item[1].lower().startswith(
                                         text.lower()))

        self.stock_list.pack(side="top", expand=1, fill="both")
        self.stock_list.bind('<Return>', self.add_to_workspace)
        self.stock_list.bind('<Double-Button-1>', self.add_to_workspace)
        self.stock_list.focus_set()

    def open_communication_with_workspace(self, workspace):
        """
        Gives stock list possibility to modify workspace. Perhaps silly solution, but will have to do for now.
        :param workspace:
        """
        self.workspace = workspace

    def add_to_workspace(self, event):
        """
        Adds clicked ticker to the workspace.
        :param event: Eventhandler.
        """
        ticker = self.stock_list.selection()[0]
        EMPTY_BOX = "\u2610"
        self.workspace.append(EMPTY_BOX + ticker)

    @staticmethod
    def load_ticker_name_info(exchange):
        """
        Fetches stock ticker and company name from an exchange and returns them as a list of namedtuples.
        :param exchange: Choice of stock exchange.
        :return: List of namedtuples with stock ticker and company name from stock exchange.
        """
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_file)
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info
