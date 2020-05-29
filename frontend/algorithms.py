import sys
sys.path.append("..")

import os

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from backend import stock_data as sd


class AlgorithmWindow:

    def __init__(self, root):
        self.root = root
        self.PlotWindow = PlotWindow(root)
        self.AlgorithmBox = AlgorithmBox(root)
        self.Buttons = Buttons(root)


class PlotWindow:

    def __init__(self, root):

        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack(side="left", anchor=tk.NW)

        # Initialize stock window with Apple stock data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.a = self.figure.add_subplot(111)
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

    def __init__(self, root):
        self.root = root
        self.stock_box_frame = tk.Frame(self.root)
        self.stock_box_frame.pack(anchor=tk.NE)

        files = os.listdir("../algorithms")
        self.stock_list = FilterList(self.stock_list_frame,
                source=files,
                display_rule=lambda item: item[0] + " | " + item[1],
                filter_rule=lambda item, text:
                            item[0].lower().startswith(text.lower()) or item[1].lower().startswith(text.lower()))
        
        self.stock_list.pack(side="top", expand=1, fill="both")


