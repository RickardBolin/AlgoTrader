import tkinter as tk
from stock_workspace import StockWorkspace
from algorithm_workspace import AlgorithmWorkspace


class Workspaces:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspaces_frame):
        self.stock_workspace = StockWorkspace(workspaces_frame)
        self.button_frame = tk.Frame(workspaces_frame)
        self.button_frame.pack()
        self.update_button = tk.Button(self.button_frame, text="Update Plot")
        self.update_button.grid(row=0, column=0)#(expand=1, fill="x")
        self.update_button.bind('<Button-1>', self.update_plot)

        self.hold_on_button = tk.Checkbutton(self.button_frame, text="Hold on")
        self.hold_on_button.grid(row=0, column=1)
        self.hold_on_button.bind('<Button-1>', self.toggle_hold_on)
        self.hold_on = False

        self.algorithm_workspace = AlgorithmWorkspace(workspaces_frame)

        self.test_algorithm_button = tk.Button(workspaces_frame, text="Test Algorithm")
        self.test_algorithm_button.pack(expand=1, fill="x")
        self.test_algorithm_button.bind('<Button-1>', self.test_algorithms)

    def update_plot(self, event):
        self.stock_workspace.update_plot(self.hold_on)

    def test_algorithms(self, event):
        self.algorithm_workspace.test_algorithms(self.stock_workspace.selected)
        self.algorithm_workspace.update_plot(self.hold_on)

    def toggle_hold_on(self, event):
        self.hold_on = not self.hold_on


