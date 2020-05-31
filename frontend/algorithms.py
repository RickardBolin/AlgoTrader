import sys


sys.path.append("..")

import os

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from backend import stock_data as sd
from tkfilterlist import FilterList
from backend import backtest
from trading_algorithms.gustafs_moneymaker.main import Bot
from datetime import datetime
import pandas as pd
import numpy as np


class AlgorithmWindow:

    def __init__(self, root):
        self.root = root
        self.PlotWindow = AlgorithmPlot(root)
        self.AlgorithmList = AlgorithmList(root, self)


class AlgorithmPlot:
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

    def update_algorithm_plot(self, tickers):
        """
        UNFINISHED
        Updates the stock plot to the specified tickers.
        Shall also be expanded to allow specifications of dates, interval etc.
        :param tickers: Stock tickers of stock to be plotted.
        """
        item = self.AlgorithmList.stock_list.selection()
        bot = self.load_agent(item)
        actions = backtest.backtest(Bot(), ["AAPL"])
        x = []
        y = []
        for info, position in actions:
            x.append(self.convert_unix_to_timestamp(info[0]))
            y.append(info[2])

        stock_data = sd.get_stock_data("AAPL", start="2019-05-25", interval="1d")
        self.PlotWindow.a.plot(stock_data["Close"])
        self.PlotWindow.a.plot(stock_data["Close"].keys()[10:-10],
                               self.moving_average(stock_data["Close"], 10)[10:-10])
        self.PlotWindow.a.plot(stock_data["Close"].keys()[20:-20],
                               self.moving_average(stock_data["Close"], 20)[20:-20])
        self.PlotWindow.a.scatter(x=x, y=y, marker='x')
        self.PlotWindow.canvas.draw()

    def percentual_change_plot(self, tickers):
        self.figure.clear()
        self.a = self.figure.add_subplot(111)

        y_max = 0
        y_min = 1e30

        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start="2016-05-25", interval="1d")
            closed_values = stock_data['Close']
            one_day_ahead_closed_values = closed_values.shift(1)
            percentual_change = 100 * (one_day_ahead_closed_values - closed_values).div(closed_values)
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


    ############# VAD SKA LIGGA?
    @staticmethod
    def moving_average(data, window):
        return np.nan_to_num(np.convolve(data, np.ones(window), 'same') / window)

    def load_agent(self, name):
        '''Loads a bot from the bots directory and validates
        its interface'''
        mod_name = "trading_algorithms." + name + ".main"
        mod = __import__(mod_name, fromlist=['Bot'])
        klass = getattr(mod, 'Bot')
        self.has_function(klass, name, "handle_event")

        return klass

    def has_function(self, module, bot_name, function_name):
        '''Checks if bot has the named function'''
        op = getattr(module, function_name, None)
        if not callable(op):
            raise NotImplementedError('Bot "{}" does not implement method: "{}"'.format(
                bot_name, function_name))

    @staticmethod
    def convert_unix_to_timestamp(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')  # %H:%M:%S'))


class AlgorithmList:

    def __init__(self, root, parent):
        self.parent = parent
        self.root = root
        self.stock_list_frame = tk.Frame(self.root)
        self.stock_list_frame.pack(anchor=tk.NE)

        files = os.listdir("../trading_algorithms")
        self.stock_list = FilterList(self.stock_list_frame,
                source=files,
                display_rule=lambda item: item,
                filter_rule=lambda item, text:
                            item.lower().startswith(text.lower()))
        
        #self.stock_list.bind('<Return>', self.parent.update_plot)
        self.stock_list.pack(side="top", expand=1, fill="both")
        self.stock_list.focus_set()


