import sys

sys.path.append("..")
import os
import tkinter as tk
from tkfilterlist import FilterList
import backend.algorithm as algo
from file_system.file_handler import read_result


class AlgorithmWindow:

    def __init__(self, root):
        self.root = root

        self.results_and_bots_frame = tk.Frame(root, height=3)
        self.results_and_bots_frame.pack(side=tk.TOP, expand=0, fill="both")

        # Create list of generated results
        self.results_frame = tk.LabelFrame(self.results_and_bots_frame, text="Results")
        self.results_frame.pack(side=tk.LEFT, fill="both")

        self.results_list = tk.Listbox(self.results_frame)
        self.results_list.pack(fill="both", expand=1)
        self.results_list.bind('<Double-Button-1>', self.read_statistics)
        self.results_list.bind('<Return>', self.read_statistics)

        # Create bot list
        self.bot_list_frame = tk.LabelFrame(self.results_and_bots_frame, text="Bots")
        self.bot_list_frame.pack(side=tk.RIGHT, expand=1, fill="both")
        algorithms = os.listdir("../file_system/trading_algorithms")
        self.list = FilterList(self.bot_list_frame,
                               source=algorithms,
                               display_rule=lambda item: item,
                               filter_rule=lambda item, text:
                               item.lower().startswith(text.lower()))

        self.list.pack(side="top", expand=1, fill="both")
        self.list.bind('<Return>', self.add_to_workspace)
        self.list.bind('<Double-Button-1>', self.add_to_workspace)

        # Create frame for buttons
        self.button_frame = tk.Frame(self.results_frame)
        self.button_frame.pack()

        self.test_algorithm_button = tk.Button(self.button_frame, text="Test Algorithm")
        self.test_algorithm_button.pack(side=tk.LEFT)
        self.test_algorithm_button.bind('<Button-1>', self.test_algorithms)

        self.plot_results_button = tk.Button(self.button_frame, text="Plot Results")
        self.plot_results_button.pack(side=tk.LEFT)
        self.plot_results_button.bind('<Button-1>', self.plot_results)

        # Create statistics box
        self.statistics_frame = tk.LabelFrame(self.root, text="Statistics")
        self.statistics_frame.pack(fill='both', expand=1)
        self.statistics_box = tk.Listbox(self.statistics_frame)
        self.statistics_box.pack(fill='both', expand=1)

    def test_algorithms(self, event):
        # Tell backend to test the algorithm
        tickers = self.workspaces.stock_workspace.selected_tickers
        start = self.workspaces.stock_workspace.start.get()

        if self.workspaces.stock_workspace.end.get() == "None":
            end = None
        else:
            end = self.workspaces.stock_workspace.end.get()

        interval = self.workspaces.stock_workspace.interval.get()
        bot_names = self.workspaces.algorithm_workspace.selected_bots
        # Results is a dictionary with bot.name as key, a tuple (timestamps, price, position) as value,
        # and each of those are themselves dictionaries with tickers as keys.
        name = "".join(bot_names)
        algo.test_algorithms(tickers=tickers, interval=interval, start=start, end=end, bot_names=bot_names, algorithm_name=name)

        ############ Lägg in att ta bort vid dublett.
        self.results_list.insert(0, name)
        self.results_list.selection_set(0)

    def plot_results(self, event):
        self.plotter.plot_result(self.results_list.get(tk.ACTIVE))

    def read_statistics(self, event):
        self.statistics_box.delete(0, tk.END)
        algorithm_results = read_result('../file_system/results/' + self.results_list.selection_get() + '.csv')
        algorithm_results = algo.calc_componentwise_percentual_profit(algorithm_results)
        for bot_name, bot_results in algorithm_results.items():
            self.statistics_box.insert(tk.END, bot_name)
            self.statistics_box.insert(tk.END, 'Profit multipliers: ')
            for ticker, multiplier in bot_results.items():
                self.statistics_box.insert(tk.END, ticker + ': ' + f'{multiplier:.2f}')

    def open_communication_with_plotter(self, plotter):
        """
        Functions which lets the plot communicate the algorithm workspace.
        :param algorithm_workspace: AlgorithmWorkspace.
        """
        self.plotter = plotter

    def open_communication_with_workspaces(self, workspaces):
        """
        Functions which lets the plot communicate the workspaces.
        :param workspaces: Workspaces.
        """
        self.workspaces = workspaces

    def add_to_workspace(self, event):
        """
        Adds clicked ticker to the workspace.
        :param event: Eventhandler.
        """
        algorithm = self.list.selection()
        EMPTY_BOX = "\u2610"
        self.algorithm_workspace.add(EMPTY_BOX + algorithm)

    def open_communication_with_algorithm_workspace(self, algorithm_workspace):
        """
        Functions which lets the algorithm list modify the algorithm workspace.
        :param algorithm_workspace: Algorithm Workspace.
        """
        self.algorithm_workspace = algorithm_workspace

