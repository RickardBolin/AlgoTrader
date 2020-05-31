import tkinter as tk


class Workspace:
    """
    Workspace class which handels the workspace, makes sense to have as a seperate file and class. However unsure
    about what do with about the dependencies. I added an "open-communication" to allow for workspace to
    change graph. This might be dumb, but it'll suffice for now i guess.
    """

    def __init__(self, workspace_frame):
        self.selected = []
        self.workspace_list = tk.Listbox(workspace_frame, height=30)
        self.update_button = tk.Button(workspace_frame, text="Update Plot")
        self.workspace_label = tk.Label(workspace_frame, text="Workspace")

        self.workspace_label.pack(expand=1, fill="both")
        self.workspace_list.pack(expand=1, fill="both")
        self.update_button.pack(expand=1, fill="x")

        self.update_button.bind('<Button-1>', self.plot_stock)
        self.workspace_list.bind('<BackSpace>', self.remove)
        self.workspace_list.bind('<Return>', self.select)
        self.workspace_list.bind('<Double-Button-1>', self.select)
        self.workspace_list.bind('<P>', self.plot_stock)

        self.workspace_list.focus_set()

    def open_communication_with_stock_window(self, stock_window):
        """
        Functions which lets the workspace modify the stock_window.
        :param stock_window: Stock window.
        """
        self.stock_window = stock_window

    def plot_stock(self, event):
        """
        Plots selected stocks.
        :param event: Eventhandle.
        """
        stock_plot = self.stock_window.stock_plot
        plot_style = stock_plot.plot_style.get()
        if plot_style == 'Regular':
            stock_plot.update_stock_plot(self.selected)
        else:
            stock_plot.subtracted_means_plot(self.selected)

    def append(self, elem):
        """
        Adds an element at the end of the workspace.
        :param elem: Element to append.
        """
        if elem not in self.workspace_list.get(0, tk.END):
            self.workspace_list.insert(tk.END, elem)

    def remove(self, event):
        """
        Removes highlighted element from the workspace.
        """
        highlighted_idx = self.workspace_list.curselection()[0]
        highlighted_elem = self.workspace_list.get(highlighted_idx)[1:]
        self.workspace_list.delete(highlighted_idx)
        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)

    def remove_all(self, event):
        """
        Removes all elements from the workspace
        """
        self.workspace_list.delete(0, tk.END)

    def select(self, event):
        EMPTY_BOX = "\u2610"
        CHECKED_BOX = "\u2611"
        highlighted_elem = self.workspace_list.get(tk.ACTIVE)
        index = self.workspace_list.get(0, "end").index(highlighted_elem)
        # Make sure to not include the box in the ticker with [1:]
        highlighted_elem = highlighted_elem[1:]

        if highlighted_elem in self.selected:
            self.selected.remove(highlighted_elem)
            new_string = EMPTY_BOX + highlighted_elem

        else:
            self.selected.append(highlighted_elem)
            new_string = CHECKED_BOX + highlighted_elem

        self.workspace_list.delete(index)
        self.workspace_list.insert(index, new_string)
        self.workspace_list.activate(index)
        self.workspace_list.update()

