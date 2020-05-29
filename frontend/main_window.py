import tkinter as tk					 
from tkinter import ttk 
from ttkthemes import ThemedTk



root = ThemedTk(theme="winxpblue") 
root.style = ttk.Style()
#('clam', 'alt', 'default', 'classic')
root.title("Kompisfonden") 
tabControl = ttk.Notebook(root) 

tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 

tabControl.add(tab1, text ='Stocks') 
tabControl.add(tab2, text ='Algorithms') 
tabControl.pack(expand = 1, fill ="both") 

ttk.Label(tab1, 
	text ="Welcome to GeeksForGeeks").grid(column = 0, 
				row = 0, 
				padx = 30, 
				pady = 30) 

root.mainloop() 

