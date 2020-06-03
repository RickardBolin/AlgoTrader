import tkinter as tk


class StockWorkspace:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspace_frame):
        self.selected_tickers = []
        self.list = tk.Listbox(workspace_frame, height=15)

        self.label = tk.Label(workspace_frame, text="Stock workspace")

        self.label.pack(expand=1, fill="both")
        self.list.pack(expand=1, fill="both")

        self.plot_options_frame = tk.Frame(workspace_frame)
        self.plot_options_frame.pack()



        # BYT GRID TILL FRAME FÖR BÅDA!
        # Add button that updates the plot
        self.update_button = tk.Button(self.plot_options_frame, text="Plot Stocks")
        self.update_button.grid(row=0, column=0)
        self.update_button.bind('<Button-1>', self.plot_stocks)

        self.list.bind('<BackSpace>', self.remove)
        self.list.bind('<Return>', self.select)
        self.list.bind('<Double-Button-1>', self.select)

        # Add option menu to choose the interval between data points
        self.INTERVAL_OPTIONS = [
            '1m',
            '1d',
        ]

        self.interval = tk.StringVar(self.plot_options_frame)
        self.interval.set(self.INTERVAL_OPTIONS[1])

        self.plot_menu = tk.OptionMenu(self.plot_options_frame, self.interval, *self.INTERVAL_OPTIONS)
        self.plot_menu.grid(row=0, column=1)

        # Add label and entry to choose start date
        self.start_label = tk.Label(self.plot_options_frame, text="Start date:", width=7)
        self.start_label.grid(row=1, column=0)
        self.start = tk.StringVar()
        self.start.set("2019-04-20")

        self.param_box = tk.Entry(self.plot_options_frame, textvariable=self.start, width=10)
        self.param_box.grid(row=1, column=1)

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
        if highlighted_elem in self.selected_tickers:
            self.selected_tickers.remove(highlighted_elem)

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

        if highlighted_elem in self.selected_tickers:
            self.selected_tickers.remove(highlighted_elem)
            new_string = EMPTY_BOX + highlighted_elem

        else:
            self.selected_tickers.append(highlighted_elem)
            new_string = CHECKED_BOX + highlighted_elem

        self.list.delete(index)
        self.list.insert(index, new_string)
        self.list.activate(index)
        self.list.update()

    def plot_stocks(self, event):
        self.plotter.plot_stocks(self.selected_tickers, interval=self.interval.get(), start=self.start.get())

    def open_communication_with_plotter(self, plotter):
        """
        Functions which lets the plot communicate the algorithm workspace.
        :param algorithm_workspace: AlgorithmWorkspace.
        """
        self.plotter = plotter
