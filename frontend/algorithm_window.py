import sys
sys.path.append("..")
import os
import tkinter as tk
from tkfilterlist import FilterList


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

        algorithms = os.listdir("../trading_algorithms")
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

        self.test_algorithm_button = tk.Button(self.results_frame, text="Test Algorithm")
        self.test_algorithm_button.pack(expand=1, fill="x")
        self.test_algorithm_button.bind('<Button-1>', self.test_algorithms)

        self.plot_results_button = tk.Button(self.results_frame, text="Plot Results")
        self.plot_results_button.pack(expand=1, fill="x")
        self.plot_results_button.bind('<Button-1>', self.plot_results)

        # SHOULD BE REMOVED WHEN WE HAVE A FILE SYSTEM
        self.results = None

    def test_algorithms(self, event):
        # Tell backend to test the algorithm
        tickers = self.workspaces.stock_workspace.selected_tickers
        bot_names = self.workspaces.algorithm_workspace.selected_bots
        # Results is a dictionary with bot.name as key, a tuple (timestamps, price, position) as value,
        # and each of those are themselves dictionaries with tickers as keys.

        #####
        # SHOULD BE REMOVED WHEN WE HAVE A FILE SYSTEM
        self.results = self.backend.test_algorithms(tickers, bot_names)
        #####
        self.results_list.insert(0, "test")

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

    def open_communication_with_backend(self, backend):
        """
        Functions which lets the plot communicate the backend.
        :param backend: Backend.
        """
        self.backend = backend

