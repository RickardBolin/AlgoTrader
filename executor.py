import tkinter
from importlib import reload
from frontend.main_window import MainWindow
import backend
import file_system
import frontend
import sys


class Executor:
    def __init__(self):
        self.root = tkinter.Tk()
        self.app = MainWindow(master=self.root, reload=self.on_reload)
        self.app.mainloop()

    def on_reload(self, event):
        self.root.destroy()
        self.root = tkinter.Tk()
        self.app = MainWindow(master=self.root, reload=self.on_reload)
        self.app.mainloop()

if __name__ == '__main__':
    Executor()