import sys
import csv
sys.path.append("..")

import tkinter as tk
from collections import namedtuple
from tkfilterlist import FilterList


class StockWindow:
    """
    POTENTIALLY UNFINISHED
    Class for the entire stock tab.
    Currently contains its tab, a stockplot and the list of stocks in an exchange.
    """

    def __init__(self, stock_tab):
        self.stock_tab = stock_tab
        self.list = StockList(self.stock_tab)


class StockList:
    """
    NB! SEVERAL FEATURES IN THIS CLASS ARE SUBJECT TO CHANGE.
    Class for the filterable stocklist.
    Contains its rootframe and the stock plot which shall be updated.
    """

    def __init__(self, root):
        self.root = root

        self.list_frame = tk.LabelFrame(self.root, text='Stocks')
        self.list_frame.pack(side="right", anchor=tk.NE, fill="y")
        stock_names = self.load_ticker_name_info("NASDAQ")
        self.list = FilterList(self.list_frame,
                                     height=27,
                                     source=stock_names,
                                     display_rule=lambda item: item[0] + ": " + item[1],
                                     filter_rule=lambda item, text:
                                     item[0].lower().startswith(text.lower()) or item[1].lower().startswith(
                                         text.lower()))

        self.list.pack(side="top", expand=1, fill="both")
        self.list.bind('<Return>', self.add_to_workspace)
        self.list.bind('<Double-Button-1>', self.add_to_workspace)

    def add_to_workspace(self, event):
        """
        Adds clicked ticker to the workspace.
        :param event: Eventhandler.
        """
        ticker = self.list.selection()[0]
        EMPTY_BOX = "\u2610"
        self.stock_workspace.add(EMPTY_BOX + ticker)

    @staticmethod
    def load_ticker_name_info(exchange):
        """
        Fetches stock ticker and company name from an exchange and returns them as a list of namedtuples.
        :param exchange: Choice of stock exchange.
        :return: List of namedtuples with stock ticker and company name from stock exchange.
        """
        with open("../Data/Tickers/" + exchange + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_file)
            company = namedtuple("company_info", ["ticker", "name"])
            stock_info = [company(stock[0], stock[1]) for stock in csv_reader]
            return stock_info

    def open_communication_with_stock_workspace(self, stock_workspace):
        """
        Gives stock list possibility to modify workspace. Perhaps silly solution, but will have to do for now.
        :param stock_workspace: StockWorkspace
        """
        self.stock_workspace = stock_workspace