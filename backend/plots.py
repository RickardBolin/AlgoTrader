import backend.stock_data as sd
from collections import defaultdict
from file_system.file_handler import read_result
import pandas as pd
import backend.timeseries as ts


def get_stocks(tickers, plot_style, params="None", start="2018-05-30", interval="1d", price_type="Close"):
    stock_data = sd.get_stock_data(tickers, start=start, interval=interval)
    stock_data = stock_data[price_type]
    # If we do not want to apply any transformation, return the regular stock data
    if plot_style == "None":
        return stock_data.index, stock_data

    ## Add error message when params = "None"?
    prices = dict()
    if len(tickers) == 1:
        prices[tickers[0]] = eval(plot_style + "(stock_data, " + params + ")")
    else:
        for ticker, _prices in stock_data.items():
            prices[ticker] = eval(plot_style + "(_prices, " + params + ")")

    return stock_data.index, pd.DataFrame.from_dict(prices)


def get_result(result_name):  # , plot_style=None):
    result = read_result('../file_system/results/' + result_name + '.csv')
    structure_results = defaultdict(defaultdict)
    for bot_name, df in result.items():
        # Loop over all stocks that the algorithm was tested on
        bot_results = defaultdict(tuple)
        for ticker in df.Ticker.unique():
            actions = df.loc[df['Ticker'] == ticker]
            # Separate long and short positions and scatter with different markers
            x_long, x_short, y_long, y_short = [], [], [], []
            for timestamp, price, position in zip(actions.index, actions['Price'], actions['Position']):
                if position == 'long':
                    x_long.append(timestamp)
                    y_long.append(price)
                else:
                    x_short.append(timestamp)
                    y_short.append(price)

            long = pd.Series(y_long, index=x_long)
            short = pd.Series(y_short, index=x_short)
            bot_results[ticker] = (long, short)
        structure_results[bot_name] = bot_results
    return structure_results

