import tkinter as tk					 
from tkinter import ttk
from stock_window import StockWindow
from algorithm_window import AlgorithmWindow
from workspaces import Workspaces
from plotter import Plotter


class MainWindow:
    def __init__(self):
        self.openGUI()

    def construct_tabs(self, root):
        tab_frame = ttk.Frame(root)
        tab_frame.pack(side='right')
        tab_control = ttk.Notebook(tab_frame)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Stocks')
        tab_control.add(tab2, text='Algorithms')
        tab_control.add(tab3, text='Portfolios')

        tab_control.pack(expand=1, fill="both")
        return StockWindow(tab1), AlgorithmWindow(tab2)

    def construct_workspace(self, root):
        workspaces_frame = ttk.Frame(root)
        workspaces_frame.pack(side='left')
        return Workspaces(workspaces_frame)

    def openGUI(self):
        root = tk.Tk()
        root.style = ttk.Style()
        # ('clam', 'alt', 'default', 'classic')
        root.title("Kompisfonden")
        workspaces = self.construct_workspace(root)
        stock_window, algorithm_window = self.construct_tabs(root)
        plotter = Plotter(root)

        # Open communications
        stock_window.list.open_communication_with_stock_workspace(workspaces.stock_workspace)
        workspaces.stock_workspace.open_communication_with_plotter(plotter)
        algorithm_window.list.open_communication_with_algorithm_workspace(workspaces.algorithm_workspace)

        algorithm_window.result_handler.open_communication_with_workspaces(workspaces)
        algorithm_window.result_handler.open_communication_with_plotter(plotter)

        root.mainloop()

test = MainWindow()
