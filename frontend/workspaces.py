import tkinter as tk
from frontend.stock_workspace import StockWorkspace
from frontend.algorithm_workspace import AlgorithmWorkspace


class Workspaces:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspaces_frame):
        self.stock_workspace = StockWorkspace(workspaces_frame)
        self.algorithm_workspace = AlgorithmWorkspace(workspaces_frame)
