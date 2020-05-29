import tkinter as tk
from functools import partial
import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from backend import stock_data as sd


class StockWindow:

    def __init__(self, root):

        self.root = root
        self.stock_frame = tk.Frame(self.root)
        self.stock_frame.pack(side=tk.BOTTOM)

        # Initialize stock window with Apple stock data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        print(self.figure)
        stock_data = sd.get_stock_data("AAPL", start="2019-05-25", interval="1d")
        self.a = self.figure.add_subplot(111)
        self.graph = self.a.plot(stock_data["Close"])
        self.canvas = FigureCanvasTkAgg(self.figure, self.stock_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_stock(self, stock):
        stock_data = sd.get_stock_data(stock, start="2019-05-25", interval="1d")
        self.graph[0].set_ydata(stock_data["Close"])
        self.a.set_ylim([0.9*min(stock_data["Close"]), 1.1*max(stock_data["Close"])])
        self.canvas.draw()


class Buttons:

    def __init__(self, root):
        self.root = root
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP)

        self.stock_label = tk.Label(self.button_frame, text="Stock ticker")
        self.stock_entry = tk.Entry(self.button_frame)

        self.stock_label.grid(row=0)
        self.stock_entry.grid(row=0, column=1)

        self.search_button = tk.Button(self.button_frame, text="Search")
        self.search_button.grid(row=1, column=0, columnspan=2)
        self.search_button.bind("<Button-1>", self.search_stock)

    def search_stock(self, event):
        stock = self.stock_entry.get()
        StockWindow.update_stock(stock)
        return 0


root = tk.Tk()
root.minsize(640, 400)
StockWindow = StockWindow(root)
Buttons = Buttons(root)
root.mainloop()
