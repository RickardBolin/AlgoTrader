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
        self.list = AlgorithmList(root)
        self.result_handler = ResultHandler(root)


class AlgorithmList:

    def __init__(self, root):
        self.root = root
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(anchor=tk.NE)

        algorithms = os.listdir("../file_system/trading_algorithms")
        self.list = FilterList(self.list_frame,
                source=algorithms,
                display_rule=lambda item: item,
                filter_rule=lambda item, text:
                            item.lower().startswith(text.lower()))

        self.list.pack(side="top", expand=1, fill="both")
        self.list.bind('<Return>', self.add_to_workspace)
        self.list.bind('<Double-Button-1>', self.add_to_workspace)

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


class ResultHandler:
    def __init__(self, root):
        self.root = root
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(anchor=tk.SE)

        self.results_list = tk.Listbox(self.results_frame, height=8)
        self.results_list.pack(anchor=tk.NW)
        self.results_list.bind('<Button-1>', self.read_statistics)

        self.statistics_box = tk.Listbox(self.results_frame, height=8)
        self.statistics_box.pack(anchor=tk.SW)

        self.test_algorithm_button = tk.Button(self.results_frame, text="Test Algorithm")
        self.test_algorithm_button.pack(expand=1, fill="x")
        self.test_algorithm_button.bind('<Button-1>', self.test_algorithms)

        self.plot_results_button = tk.Button(self.results_frame, text="Plot Results")
        self.plot_results_button.pack(expand=1, fill="x")
        self.plot_results_button.bind('<Button-1>', self.plot_results)

    def test_algorithms(self, event):
        # Tell backend to test the algorithm
        tickers = self.workspaces.stock_workspace.selected_tickers
        start = self.workspaces.stock_workspace.start.get()
        interval = self.workspaces.stock_workspace.interval.get()
        bot_names = self.workspaces.algorithm_workspace.selected_bots
        # Results is a dictionary with bot.name as key, a tuple (timestamps, price, position) as value,
        # and each of those are themselves dictionaries with tickers as keys.
        name = "".join(bot_names)
        algo.test_algorithms(tickers, start, interval, bot_names, name)

        ############ Lägg in att ta bort vid dublett.
        self.results_list.insert(0, name)
        self.results_list.selection_set(0)

    def read_statistics(self, event):
        self.statistics_box.delete(0, tk.END)
        algorithm_results = read_result('../file_system/results/' + self.results_list.selection_get() + '.csv')
        algorithm_results = algo.calc_componentwise_percentual_profit(algorithm_results)
        for bot_name, bot_results in algorithm_results.items():
            self.statistics_box.insert(tk.END, bot_name)
            self.statistics_box.insert(tk.END, 'Profit multipliers: ')
            for ticker, multiplier in bot_results.items():
                self.statistics_box.insert(tk.END, ticker + ': ' + f'{multiplier:.2f}')


    def plot_results(self, event):
        self.plotter.plot_result(self.results_list.get(tk.ACTIVE))

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


