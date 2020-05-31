import tkinter as tk
from backend import stock_data as sd

class StockWorkspace:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspace_frame):
        self.selected = []
        self.list = tk.Listbox(workspace_frame, height=15)

        self.label = tk.Label(workspace_frame, text="Stock workspace")

        self.label.pack(expand=1, fill="both")
        self.list.pack(expand=1, fill="both")

        self.list.bind('<BackSpace>', self.remove)
        self.list.bind('<Return>', self.select)
        self.list.bind('<Double-Button-1>', self.select)

    def open_communication_with_stock_window(self, stock_window):
        """
        Functions which lets the workspace modify the stock_window.
        :param stock_window: Stock window.
        """
        self.stock_window = stock_window

    def open_communication_with_plotter(self, plotter):
        """
        Functions which lets the workspace modify the plot.
        :param plotter: Plotter.
        """
        self.plotter = plotter

    def add(self, elem):
        """
        Adds an element at the end of the workspace.
        :param elem: Element to append.
        """
        stripped = [string[1:] for string in self.list.get(0, tk.END)]
        if elem[1:] not in stripped:
            self.list.insert(tk.END, elem)

    def remove(self, event):
        """
        Removes highlighted element from the workspace.
        """
        highlighted_idx = self.list.curselection()[0]
        highlighted_elem = self.list.get(highlighted_idx)[1:]
        self.list.delete(highlighted_idx)
        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)

    def remove_all(self, event):
        """
        Removes all elements from the workspace
        """
        self.list.delete(0, tk.END)

    def select(self, event):
        EMPTY_BOX = "\u2610"
        CHECKED_BOX = "\u2611"
        highlighted_elem = self.list.get(tk.ACTIVE)
        index = self.list.get(0, "end").index(highlighted_elem)
        # Make sure to not include the box in the ticker with [1:]
        highlighted_elem = highlighted_elem[1:]

        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)
            new_string = EMPTY_BOX + highlighted_elem

        else:
            self.selected.append(highlighted_elem)
            new_string = CHECKED_BOX + highlighted_elem

        self.list.delete(index)
        self.list.insert(index, new_string)
        self.list.activate(index)
        self.list.update()

    def update_plot(self):
        """
        Plots selected stocks.
        """
        plot_style = self.plotter.plot_style.get()
        if plot_style == 'Regular':
            self.plot_regular_stock(self.selected)
        else:
            self.plot_percentual_change(self.selected)

    def plot_regular_stock(self, tickers, start="2016-05-25", interval="1d"):
        """
        UNFINISHED
        """
        data = dict()
        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
            data[ticker] = stock_data["Close"]
        self.plotter.update_plot(data)

    def plot_percentual_change(self, tickers, start="2016-05-25", interval="1d"):
        data = dict()
        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
            closed_values = stock_data['Close']
            one_day_ahead_closed_values = closed_values.shift(-1)
            percentual_change = 100*(one_day_ahead_closed_values - closed_values).div(closed_values)
            percentual_change = percentual_change.dropna()
            data[ticker] = percentual_change
        self.plotter.update_plot(data)


