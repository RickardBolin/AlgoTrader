import tkinter as tk					 
from tkinter import ttk
from frontend.stock_window import StockWindow
from frontend.algorithm_window import AlgorithmWindow
from frontend.workspaces import Workspaces
from frontend.plotter import Plotter
from frontend.console import Console
import os
from importlib import reload
import sys

class MainWindow(tk.Frame):
    def __init__(self, master=None, reload=None):
        root = tk.Frame.__init__(self, master)
        self.master.title("Kompisfonden")
        self.master.bind("<Control-R>", reload)
        self.pack()

        self.openGUI(self)

    def construct_tabs(self, root):
        tab_frame = ttk.Frame(root)
        tab_frame.pack(side=tk.RIGHT, fill="both")
        tab_control = ttk.Notebook(tab_frame)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)
        tab4 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Stocks')
        tab_control.add(tab2, text='Algorithms')
        tab_control.add(tab3, text='Portfolios')
        tab_control.add(tab4, text="Console")

        tab_control.pack(expand=1, fill="both")
        return StockWindow(tab1), AlgorithmWindow(tab2), Console(tab4)

    def construct_workspace(self, root):
        workspaces_frame = ttk.Frame(root)
        workspaces_frame.pack(side=tk.LEFT)
        return Workspaces(workspaces_frame)

    def openGUI(self, root):
        self.root = root
        workspaces = self.construct_workspace(self.root)
        stock_window, algorithm_window, console = self.construct_tabs(self.root)
        plotter = Plotter(self.root)

        # Open communications
        stock_window.list.open_communication_with_stock_workspace(workspaces.stock_workspace)
        workspaces.stock_workspace.open_communication_with_plotter(plotter)
        algorithm_window.open_communication_with_algorithm_workspace(workspaces.algorithm_workspace)

        algorithm_window.open_communication_with_workspaces(workspaces)
        algorithm_window.open_communication_with_plotter(plotter)

        console.open_communication_with_stock_workspace(workspaces.stock_workspace)

        #self.root.mainloop()

#MainWindow()
