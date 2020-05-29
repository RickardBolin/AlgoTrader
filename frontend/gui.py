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
        self.stock_label = tk.Label(self.root, text="Stock ticker")
        self.stock_entry = tk.Entry(self.root)

        self.stock_label.grid(row=0)
        self.stock_entry.grid(row=0, column=1)

        self.search_button = tk.Button(self.root, text="Search")
        self.search_button.grid(row=1, column=0, columnspan=2)
        self.search_button.bind("<Button-1>", self.search_stock)

    def search_stock(self, event):
        stock = self.stock_entry.get()
        self.plot_stock()
        print("Stock: " + stock)
        return 0

    def plot_stock(self):
        f = Figure(figsize=(5,5), dpi=100)
        stock_data = sd.get_stock_data(self.stock_entry.get(), start="2019-05-25", interval="1d")
        f.add_subplot(111).plot(stock_data)

        canvas = FigureCanvasTkAgg(f, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


root = tk.Tk()
StockWindow(root)

root.mainloop()
