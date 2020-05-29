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

        self.stock_box = tk.Listbox(self.stock_box_frame, width=27, height=27)
        self.stock_box.pack(side="left")

        self.stock_scroller = tk.Scrollbar(self.stock_box_frame, orient="vertical")
        self.stock_scroller.config(command=self.stock_box.yview)
        self.stock_scroller.pack(side="right", fill="y")

        self.stock_box.config(yscrollcommand=self.stock_scroller.set)

        files = os.listdir("../algorithms")
        for i,alg in enumerate(files):
            self.stock_box.insert(i, alg)

