from backend import stock_data as sd
from collections import defaultdict, namedtuple
from datetime import datetime
import backend.algorithm as algo
import backend.utils as utils
import backend.plots as plots
from file_system.file_handler import read_result


class Backend:
    # TA BORT RESULTS SEN NÄR VI FIXAT FILSYSTEM
    def __init__(self, results_handler):
        self.results_handler = results_handler

    def get_result(self, result_name):  # , plot_style=None):
        #####
        # ONLY THIS SHOULD BE REPLACED WITH A FUNCTION THAT READS FROM FILE
        result = read_result('../file_system/results/test.csv')
        #####
        structured_results = defaultdict(tuple)
        for bot_name, (timestamps, prices, positions) in result.items():
            # Loop over all stocks that the algorithm was tested on
            for ticker in timestamps:
                x_long, x_short, y_long, y_short = [], [], [], []

                # Separate long and short positions and scatter with different markers
                for price, position, timestamp in zip(prices[ticker], positions[ticker], timestamps[ticker]):
                    if position == "long":
                        x_long.append(timestamp)
                        y_long.append(price)
                    else:
                        x_short.append(timestamp)
                        y_short.append(price)
                structured_results[ticker] = (x_long, x_short, y_long, y_short)
        return structured_results



