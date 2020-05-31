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
        self.list = AlgorithmList(root)


class AlgorithmList:

    def __init__(self, root):
        self.root = root
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(anchor=tk.NE)

        algorithms = os.listdir("../trading_algorithms")
        self.list = FilterList(self.list_frame,
                source=algorithms,
                display_rule=lambda item: item,
                filter_rule=lambda item, text:
                            item.lower().startswith(text.lower()))

        self.list.pack(side="top", expand=1, fill="both")
        self.list.bind('<Return>', self.add_to_workspace)
        self.list.bind('<Double-Button-1>', self.add_to_workspace)

    def add_to_workspace(self, event):
        """
        Adds clicked ticker to the workspace.
        :param event: Eventhandler.
        """
        algorithm = self.list.selection()
        EMPTY_BOX = "\u2610"
        self.workspaces.algorithm_workspace.add(EMPTY_BOX + algorithm)

    def open_communication_with_workspaces(self, workspaces):
        """
        Functions which lets the workspace modify the stock_window.
        :param stock_window: Stock window.
        """
        self.workspaces = workspaces










############# VAD SKA LIGGA?
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

def convert_unix_to_timestamp(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')  # %H:%M:%S'))


def rille_ma(self, tickers):
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