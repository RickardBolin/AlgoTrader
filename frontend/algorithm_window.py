import sys
sys.path.append("..")
import os
import tkinter as tk
from tkfilterlist import FilterList


class AlgorithmWindow:

    def __init__(self, root):
        self.root = root
        self.list = AlgorithmList(root)


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
        self.workspaces.algorithm_workspace.add(EMPTY_BOX + algorithm)

    def open_communication_with_workspaces(self, workspaces):
        """
        Functions which lets the workspace modify the stock_window.
        :param stock_window: Stock window.
        """
        self.workspaces = workspaces
