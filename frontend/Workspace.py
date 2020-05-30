import tkinter as tk


class Workspace:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """
    def __init__(self, workspace_frame):
        self.workspace_list = tk.Listbox(workspace_frame, height=30)
        self.workspace_list.pack(side="top", expand=1, fill="both")
        self.workspace_list.bind('<BackSpace>', self.remove)
        self.workspace_list.bind('<Return>', self.plot_stock)
        self.workspace_list.focus_set()

    def open_communication_with_stock_window(self, stock_window):
        """
        Functions which lets the workspace modify the stock_window.
        :param stock_window: Stock window.
        """
        self.stock_window = stock_window

    def plot_stock(self, event):
        """
        Adds plot of highlighted stock.
        :param event: Eventhandle.
        """
        selected_ticker = self.workspace_list.selection_get()[0]
        self._plot_stock(selected_ticker)

    def _plot_stock(self, tickers):
        """
        Updates the plot with granted tickers.
        :param tickers: Tickers of stocks to be plotted.
        """
        self.stock_window.stock_plot.update_stock_plot(tickers)

    def append(self, elem):
        """
        Adds an element at the end of the workspace.
        :param elem: Element to append.
        """
        if elem not in self.workspace_list.get(0, tk.END):
            self.workspace_list.insert(tk.END, elem)

    def remove(self, event):
        """
        Removes highlighted element from the workspace.
        """
        highlighted_idx = self.workspace_list.curselection()[0]
        self.workspace_list.delete(highlighted_idx)

    def remove_all(self, event):
        """
        Removes all elements from the workspace
        """
        self.workspace_list.delete(0, tk.END)





