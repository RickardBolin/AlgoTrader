import backend.utils as utils
import backend.stock_data as sd
from collections import defaultdict, namedtuple


def get_event_list(tickers, start="2016-05-25", interval="1d"):
    event_list = []
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        for timestamp, new_price in stock_data["Close"].iteritems():
            unix_time = utils.convert_timestamp_to_unix(timestamp)
            event_list.append([unix_time, ticker, new_price])
    event_list.sort(key=lambda x: x[0])
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


def test_algorithms(tickers, bot_names):

    # Load all bots that are selected in the workspace
    bots = [load_agent(name)() for name in bot_names]
    # Get dictionary of the actions that each bot made, where the bot name is the key
    actions = backtest(bots, tickers)

    results = defaultdict(tuple)
    result = namedtuple("Result", ["timestamp", "price", "position"])

    for bot in bots:
        x = defaultdict(list)
        y = defaultdict(list)
        positions = defaultdict(list)

        for (time, ticker, price), position in actions[bot.name]:
            x[ticker].append(utils.convert_unix_to_timestamp(time))
            # Append new price to y
            y[ticker].append(price)
            positions[ticker].append(position)

        results[bot.name] = result(x, y, positions)
    return results


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