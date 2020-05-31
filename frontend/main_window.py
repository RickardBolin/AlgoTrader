import tkinter as tk					 
from tkinter import ttk
from Stocks import StockWindow
from algorithms import AlgorithmWindow
from Workspace import Workspace


def construct_tabs(root):
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


def construct_workspace(root):
    workspace_frame = ttk.Frame(root)
    workspace_frame.pack(side='left')
    return Workspace(workspace_frame)


if __name__ == '__main__':
    root = tk.Tk()
    root.style = ttk.Style()
    # ('clam', 'alt', 'default', 'classic')
    root.title("Kompisfonden")
    workspace = construct_workspace(root)
    stock_window, algorithm_window = construct_tabs(root)

    # Open communications
    stock_window.stock_list.open_communication_with_workspace(workspace)
    workspace.open_communication_with_stock_window(stock_window)

    root.mainloop()

