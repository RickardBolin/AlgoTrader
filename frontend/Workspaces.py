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
        self.algorithm_workspace = AlgorithmWorkspace(workspaces_frame)

        self.update_button = tk.Button(workspaces_frame, text="Update Plot")
        self.update_button.pack(expand=1, fill="x")
        self.update_button.bind('<Button-1>', self.update_plot)

    def update_plot(self, event):
        self.stock_workspace.update_plot()
        self.algorithm_workspace.update_plot()
