import sys

sys.path.append("..")

import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters

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
        self.plot_style = tk.StringVar(self.plot_frame)
        self.plot_style.set(self.PLOT_OPTIONS[0])

        self.plot_menu = tk.OptionMenu(self.plot_frame, self.plot_style, *self.PLOT_OPTIONS)
        self.plot_menu.pack(anchor=tk.NW)


    # Type: Stock or algorithm, come up with better name later
    def update_plot(self, data, type, hold_on=False):
        # If hold-on checkbox is not checked, plot to the current figure
        if not hold_on:
            self.figure.clear()
            self.a = self.figure.add_subplot(111)

        # If "data" is a dictionary, we expect it to have tickers as keys and pandas.Series-objects as values
        if type == "Stock":
            for ticker, series in data.items():
                self.a.plot(series, label=ticker)
        # If "data" is a (named)tuple, we expect it to contain the results of a backtested algorithm
        # on the form (timestamps, price, position)
        elif type == "Algorithm_results":
            for bot, actions in data.items():
                timestamps, prices, positions = actions
                # Loop over all stocks that the algorithm was tested on
                for ticker in timestamps:
                    x_long, x_short, y_long, y_short = [], [], [], []

                    # Separate long and short positions and scatter with different markers
                    for price, position, timestamp in zip(prices[ticker], positions[ticker], timestamps[ticker]):
                        if position == "long":
                            x_long.append(timestamp)
                            y_long.append(price)
                        else:
                            x_short.append(timestamp)
                            y_short.append(price)
                    self.a.scatter(x_long, y_long, marker='o')
                    self.a.scatter(x_short, y_short, marker='x')
        else:
            print("Wrong type!")

        self.a.legend()
        self.a.set_ylabel('$')
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
