import backend.stock_data as sd
from collections import defaultdict


def get_stocks(tickers, plot_style):
    if plot_style == "Regular":
        return regular_stock(tickers)
    else:
        return percentual_change(tickers)

'''
# Will need result_name-parameter later when we have a file-system!
def get_result(result_name):  # , plot_style=None):
    #####
    # ONLY THIS SHOULD BE REPLACED WITH A FUNCTION THAT READS FROM FILE
    result = self.results_handler.results
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
'''


def regular_stock(tickers, start="2016-05-25", interval="1d"):
    """
    UNFINISHED
    """
    data = dict()
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        data[ticker] = stock_data["Close"]
    return data


def percentual_change(tickers, start="2016-05-25", interval="1d"):
    data = dict()
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        closed_values = stock_data['Close']
        one_day_ahead_closed_values = closed_values.shift(-1)
        percent_change = 100 * (one_day_ahead_closed_values - closed_values).div(closed_values)
        percent_change = percent_change.dropna()
        data[ticker] = percent_change
    return data
