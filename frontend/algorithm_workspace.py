import tkinter as tk


class AlgorithmWorkspace:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspace_frame):
        self.selected = []

        self.list = tk.Listbox(workspace_frame, height=15)
        self.label = tk.Label(workspace_frame, text="Algorithm workspace")

        self.label.pack(expand=1, fill="both")
        self.list.pack(expand=1, fill="both")

        self.list.bind('<BackSpace>', self.remove)
        self.list.bind('<Return>', self.select)
        self.list.bind('<Double-Button-1>', self.select)

    def open_communication_with_plotter(self, plotter):
        """
        Functions which lets the workspace modify the plot.
        :param plotter: Plotter.
        """
        self.plotter = plotter

    def update_plot(self):
        """
        Plots selected stocks.
        :param event: Eventhandle.
        """

        plot_style = self.plotter.plot_style.get()
        if plot_style == 'Regular':
            pass
            #self.plotter.update_stock_plot(self.selected)
        else:
            pass
            #self.plotter.percentual_change_plot(self.selected)

    def add(self, elem):
        """
        Adds an element at the end of the workspace.
        :param elem: Element to append.
        """
        stripped = [string[1:] for string in self.list.get(0, tk.END)]
        if elem[1:] not in stripped:
            self.list.insert(tk.END, elem)

    def remove(self, event):
        """
        Removes highlighted element from the workspace.
        """
        highlighted_idx = self.list.curselection()[0]
        highlighted_elem = self.list.get(highlighted_idx)[1:]
        self.list.delete(highlighted_idx)
        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)

    def remove_all(self, event):
        """
        Removes all elements from the workspace
        """
        self.list.delete(0, tk.END)

    def select(self, event):
        EMPTY_BOX = "\u2610"
        CHECKED_BOX = "\u2611"
        highlighted_elem = self.list.get(tk.ACTIVE)
        index = self.list.get(0, "end").index(highlighted_elem)
        # Make sure to not include the box in the ticker with [1:]
        highlighted_elem = highlighted_elem[1:]

        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)
            new_string = EMPTY_BOX + highlighted_elem

        else:
            self.selected.append(highlighted_elem)
            new_string = CHECKED_BOX + highlighted_elem

        self.list.delete(index)
        self.list.insert(index, new_string)
        self.list.activate(index)
        self.list.update()

