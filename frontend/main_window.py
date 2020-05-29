import tkinter as tk					 
from tkinter import ttk
from Stocks import StockWindow
from algorithms import AlgorithmWindow

root = tk.Tk()
root.style = ttk.Style()
#('clam', 'alt', 'default', 'classic')
root.title("Kompisfonden") 
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)


tabControl.add(tab1, text='Stocks')
tabControl.add(tab2, text='Algorithms')
tabControl.add(tab3, text='Portfolios')

tabControl.pack(expand=1, fill="both")

Stocks = StockWindow(tab1)
Algorithms = AlgorithmWindow(tab2)

root.mainloop()

