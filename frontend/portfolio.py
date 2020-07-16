import backend.portfolio_management.efficient_frontier as ef
import backend.data_handler.stock_data as sd
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class Portfolio:

    def __init__(self, portfolio_window):

        self.plot_frame = tk.Frame(portfolio_window)
        # Add empty figure

        self.figure = plt.Figure()

        self.figure_frame = tk.LabelFrame(self.plot_frame, text="Plots")
        self.figure_frame.pack(side=tk.BOTTOM, expand=1, fill=tk.BOTH)
        self.canvas = FigureCanvasTkAgg(self.figure, self.figure_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.generate_button = tk.Button(portfolio_window, text='Generate Portfolio', command=self.generate_new)
        self.generate_button.pack()
        
        self.plot_frame.pack()

        self.portfolio = pd.DataFrame()
        self.ef = None
        self.stocks = None
        self.tickers = None
        self.weights = None

    def generate_new(self):
        self.stocks = sd.get_stock_data(self.stock_workspace.selected_tickers)['Close']
        self.ef = ef.EfficientFrontier(self.stocks)
        self.tickers = self.stocks.columns
        self.weights = self.ef.p_allocation
        self.portfolio = pd.DataFrame(self.weights, columns=self.tickers)
        self.plot()

    def plot(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        pie_ax = self.ax.pie(self.weights, labels=self.tickers, autopct='%1.1f%%')
        self.figure.legend(pie_ax[0], self.tickers, loc='upper right')
        self.canvas.draw()

    def open_communication_with_stock_workspace(self, stock_workspace):
        self.stock_workspace = stock_workspace