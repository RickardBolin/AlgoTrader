from backend import stock_data as sd
from backend.backtest import backtest
from collections import defaultdict, namedtuple
from datetime import datetime


class Backend:
    # TA BORT RESULTS SEN NÄR VI FIXAT FILSYSTEM
    def __init__(self, results_handler):
        self.results_handler = results_handler

    def get_stocks(self, tickers, plot_style):
        if plot_style == "Regular":
            return self.regular_stock(tickers)
        else:
            return self.percentual_change(tickers)


    # Will need result_name-parameter later when we have a file-system!
    def get_result(self, result_name):#, plot_style=None):
        #####
        # ONLY THIS SHOULD BE REPLACED WITH A FUNCTION THAT READS FROM FILE
        result = self.results_handler.results
        print(result)
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

    # Kan bara hantera en algorithm åt gången atm!
    def test_algorithms(self, tickers, bot_names):

        # Load all bots that are selected in the workspace
        bots = [self.load_agent(name)() for name in bot_names]
        # Get dictionary of the actions that each bot made, where the bot name is the key
        actions = backtest(bots, tickers)

        results = defaultdict(tuple)
        result = namedtuple("Result", ["timestamp", "price", "position"])

        for bot in bots:
            x = defaultdict(list)
            y = defaultdict(list)
            positions = defaultdict(list)

            for (time, ticker, price), position in actions[bot.name]:
                x[ticker].append(self.convert_unix_to_timestamp(time))
                # Append new price to y
                y[ticker].append(price)
                positions[ticker].append(position)

            results[bot.name] = result(x, y, positions)
        return results

    def load_agent(self, name):
        """
        Loads a bot from the bots directory and validates
        its interface
        """
        mod_name = "trading_algorithms." + name + ".bot"
        mod = __import__(mod_name, fromlist=['Bot'])
        klass = getattr(mod, 'Bot')
        self.has_function(klass, name, "handle_event")

        return klass

    def has_function(self, module, bot_name, function_name):
        """
        Checks if bot has the named function
        """
        op = getattr(module, function_name, None)
        if not callable(op):
            raise NotImplementedError('Bot "{}" does not implement method: "{}"'.format(
                bot_name, function_name))

    @staticmethod
    def convert_unix_to_timestamp(unix_time):
        return datetime.utcfromtimestamp(unix_time)

    def regular_stock(self, tickers, start="2016-05-25", interval="1d"):
        """
        UNFINISHED
        """
        data = dict()
        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
            data[ticker] = stock_data["Close"]
        return data

    def percentual_change(self, tickers, start="2016-05-25", interval="1d"):
        data = dict()
        for ticker in tickers:
            stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
            closed_values = stock_data['Close']
            one_day_ahead_closed_values = closed_values.shift(-1)
            percent_change = 100 * (one_day_ahead_closed_values - closed_values).div(closed_values)
            percent_change = percent_change.dropna()
            data[ticker] = percent_change
        return data