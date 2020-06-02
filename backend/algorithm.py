import backend.utils as utils
import backend.stock_data as sd
from collections import defaultdict, namedtuple
from file_system.file_handler import write_result, read_result
import math


def get_event_list(tickers, start="2018-05-30", interval="1d"):
    event_list = []
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        for timestamp, new_price in stock_data["Close"].iteritems():
            _datetime = utils.convert_timestamp_to_datetime(timestamp)
            event_list.append([_datetime, ticker, new_price])
    event_list.sort(key=lambda x: x[0])
    for i, (datetime, _, _) in enumerate(event_list):
        event_list[i][0] = utils.convert_datetime_to_timestamp(datetime)
    return event_list


def backtest(bots, tickers):
    # Get price changes of all stocks sorted by time
    event_list = get_event_list(tickers)
    # Loop over each event and let each bot handle it
    for event in event_list:
        for bot in bots:
            bot.handle_event(event)
    # Save all the different bot.actions in a dictionary
    actions = dict()
    for bot in bots:
        actions[bot.name] = bot.actions
    return actions


def test_algorithms(tickers, bot_names, algorithm_name):

    # Load all bots that are selected in the workspace
    bots = [load_agent(name)() for name in bot_names]
    # Get dictionary of the actions that each bot made, where the bot name is the key
    actions = backtest(bots, tickers)

    results = defaultdict(tuple)
    result = namedtuple("Results", ["timestamps", "prices", "positions"])

    for bot in bots:
        timestamps = defaultdict(list)
        prices = defaultdict(list)
        positions = defaultdict(list)

        for (timestamp, ticker, price), position in actions[bot.name]:
            timestamps[ticker].append(timestamp)#utils.convert_datetime_to_timestamp(datetime))
            # Append new price to y
            prices[ticker].append(price)
            positions[ticker].append(position)

        results[bot.name] = result(timestamps, prices, positions)
    write_result('../file_system/results/' + algorithm_name + '.csv', results)


def calc_componentwise_percentual_profit(results):
    """
    Calculates the compnentwise percentual profit. Assumed to have the form dict(bots)
    with (bot_name, actions_tuple) as key value pairs. Thereafter actions_tuple has the appearence of
    (timestamps, prices, positions) where each of these are a dictionary with ticker as key
    and a list of values as value.
    :param results: result dict.
    :return: Component-wise percentual profit. Dict of bots where each bot has ha dict of results for each stock.
    """

    percentual_profits = defaultdict(defaultdict)
    investment_start_price = defaultdict(defaultdict)
    for bot_name, bot_results in results.items():
        stock_percentual_profits = defaultdict(float)
        investment_stock_start_prices = defaultdict(float)
        timestamps, prices, positions = bot_results
        for ticker in timestamps:
            stock_prices, stock_positions = prices[ticker], positions[ticker]
            profit = 0
            if stock_positions[0] == 'long':
                sign = 1
            else:
                sign = -1

            for shift, price in enumerate(stock_prices[:-1], start=1):
                profit += sign*(stock_prices[shift] - price)
                sign *= -1
            stock_percentual_profits[ticker] = profit/stock_prices[0]
            investment_stock_start_prices[ticker] = stock_prices[0]
        percentual_profits[bot_name] = stock_percentual_profits
        investment_start_price[bot_name] = investment_stock_start_prices

    return percentual_profits, investment_start_price


def calc_total_percentual_profit(results):
    """
    CLEANUP?
    Calculates the total percentual profit. Assumed to have the form dict(bots)
    with (bot_name, actions_tuple) as key value pairs. Thereafter actions_tuple has the appearence of
    (timestamps, prices, positions) where each of these are a dictionary with ticker as key
    and a list of values as value.
    :param results: result dict
    :return: Total profit out of all bots on all stocks.
    """
    percentual_profits, start_prices = calc_componentwise_percentual_profit(results)
    total_profit = 0
    total_start_price = 0

    for (bot_name, bot_results), investment_start_price in zip(percentual_profits.items(), start_prices.values()):
        for (ticker, percentual_profit), investment_stock_start_price in zip(bot_results.items(), investment_start_price.values()):
            total_profit += percentual_profit
            total_start_price += investment_stock_start_price
    return total_profit/total_start_price


def load_agent(name):
    """
    Loads a bot from the bots directory and validates
    its interface
    """
    mod_name = "file_system.trading_algorithms." + name + ".bot"
    mod = __import__(mod_name, fromlist=['Bot'])
    klass = getattr(mod, 'Bot')
    has_function(klass, name, "handle_event")
    return klass


def has_function(module, bot_name, function_name):
    """
    Checks if bot has the named function
    """
    op = getattr(module, function_name, None)
    if not callable(op):
        raise NotImplementedError('Bot "{}" does not implement method: "{}"'.format(
            bot_name, function_name))