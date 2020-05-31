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
        self.PlotWindow = PlotWindow(root)
        self.AlgorithmBox = AlgorithmBox(root, self)
        self.Buttons = Buttons(root)

    def update_plot(self, event):
        
        item = self.AlgorithmBox.stock_list.selection()
        bot = self.load_agent(item)
        actions = backtest.backtest(Bot(), ["AAPL"])
        x = []
        y = []
        for info, position in actions:
            x.append(self.convert_unix_to_timestamp(info[0]))
            y.append(info[2])

        stock_data = sd.get_stock_data("AAPL", start="2019-05-25", interval="1d")
        self.PlotWindow.a.plot(stock_data["Close"])
        self.PlotWindow.a.plot(stock_data["Close"].keys()[10:-10], self.moving_average(stock_data["Close"], 10)[10:-10])
        self.PlotWindow.a.plot(stock_data["Close"].keys()[20:-20], self.moving_average(stock_data["Close"], 20)[20:-20])
        self.PlotWindow.a.scatter(x=x, y=y, marker='x')
        self.PlotWindow.canvas.draw()

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
        return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')# %H:%M:%S'))


class PlotWindow:

    def __init__(self, root):

        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack(side="left", anchor=tk.NW)

        # Initialize stock window with Apple stock data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.a = self.figure.add_subplot(111)
        self.a.set_title("Chosen algorithm")
        self.canvas = FigureCanvasTkAgg(self.figure, self.stock_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


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


class AlgorithmBox:

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
        
        self.stock_list.bind('<Return>', self.parent.update_plot)
        self.stock_list.pack(side="top", expand=1, fill="both")
        self.stock_list.focus_set()


