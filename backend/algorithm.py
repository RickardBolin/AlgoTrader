import backend.utils as utils
import backend.stock_data as sd
from collections import defaultdict, namedtuple
from file_system.file_handler import write_result


def get_event_list(tickers, start="2019-05-30", interval="1d"):
    event_list = []
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        for timestamp, new_price in stock_data["Close"].iteritems():
            _datetime = utils.convert_timestamp_to_datetime(timestamp)
            #_datetime = _datetime.replace(hour=_datetime.hour + 4, minute=(_datetime.minute + 30)%60)
            #unix_time = utils.convert_timestamp_to_unix(timestamp)
            #event_list.append([unix_time, ticker, new_price])
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