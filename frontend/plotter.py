import sys
sys.path.append("..")

import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
import backend.plots as plot
import backend.utils as utils
import pandas as pd
import numpy as np
register_matplotlib_converters()


class Plotter:
    """
    POTENTIALLY UNFINISHED
    Class which handles the stockplot.
    """

    def __init__(self, root):
        self.root = root
        self.plot_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.plot_frame)
        self.button_frame.pack(side="bottom", anchor=tk.SE)
        self.plot_frame.pack(side="left", anchor=tk.SW)

        # Add empty figure
        self.plot_time_frame = "3 Years"
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.a = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add "hold on"-checkbutton
        self.hold_on_button = tk.Checkbutton(self.button_frame, text="Hold on")
        self.hold_on_button.grid(row=0, column=0)
        self.hold_on_button.bind('<Button-1>', self.toggle_hold_on)
        self.hold_on = False
        self.param = "None"

        # Add buttons to change viewing dates
        self.viewing_date_buttons = []
        times = ["one_min", "one_day", "one_month", "one_year", "three_years"]
        for i, time in enumerate(times):
            self.viewing_date_buttons.append(tk.Button(self.button_frame, text=time))
            self.viewing_date_buttons[i].grid(row=0, column=i+1)
            self.viewing_date_buttons[i].bind("<Button-1>", eval("self." + time + "_button"))

        self.PLOT_OPTIONS = [
            'Regular',
            'Percentual change',
            'Moving Average'
        ]
        self.PLOT_TRANSFORMATIONS = [
            'None',
            'ts.percentual_change',
            'ts.moving_average'
        ]

        self.plot_to_func = dict(zip(self.PLOT_OPTIONS, self.PLOT_TRANSFORMATIONS))

        self.plot_style = tk.StringVar(self.plot_frame)
        self.plot_style.set(self.PLOT_OPTIONS[0])

        self.plot_menu = tk.OptionMenu(self.plot_frame, self.plot_style, *self.PLOT_OPTIONS)
        self.plot_menu.pack()#row=0, column=0)

        self.param = tk.StringVar()
        self.param_box = tk.Entry(self.plot_frame, textvariable=self.param)
        self.param.set("None")
        self.param_box.pack()#row=0, column=1)

    def plot_stocks(self, tickers):
        # If hold-on checkbox is not checked, plot to the current figure
        if not self.hold_on:
            self.figure.clear()
            self.a = self.figure.add_subplot(111)

        # Get data from backend
        dates, prices = plot.get_stocks(tickers, plot_style=self.plot_to_func[
                                        self.plot_style.get()], params=self.param.get())
        # Plot the retrieved stock data)
        self.a.plot(dates, prices)
        self.a.legend(tickers)
        self.a.set_ylabel('$')
        self.a.set_xlabel('Date')
        self.canvas.draw()

    def plot_result(self, result):
        # If hold-on checkbox is not checked, plot to the current figure
        if not self.hold_on:
            self.figure.clear()
            self.a = self.figure.add_subplot(111)

        # Get result from backend
        structured_result = plot.get_result(result)#, plot_style=self.plot_style.get())
        for bot_name, bot_results in structured_result.items():
            for ticker, (long, short) in bot_results.items():
                self.a.scatter(long.index, long, marker='o')
                self.a.scatter(short.index, short, marker='x')
        #self.a.legend()
        self.a.set_ylabel('$')
        self.a.set_xlabel('Date')
        self.canvas.draw()

    # Hur slår vi ihop detta till en funktion?!
    def one_min_button(self, event):
        self.plot_time_frame = "1 min"

    def one_day_button(self, event):
        self.plot_time_frame = "1 day"
        rhs = self.a.get_xlim()[0]

        # TEMPORARY RHS, THEN WILL ALWAYS BE FROM TODAY
        window_lhs, window_rhs = self.a.get_xlim()

    def one_month_button(self, event):
        self.plot_time_frame = "1 month"

    def one_year_button(self, event):
        self.plot_time_frame = "1 Year"

    def three_years_button(self, event):
        self.plot_time_frame = "3 Years"


    def toggle_hold_on(self, event):
        self.hold_on = not self.hold_on

