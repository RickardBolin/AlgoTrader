import backend.utils as utils
import backend.stock_data as sd
from collections import defaultdict
from file_system.file_handler import write_result
import pandas as pd


def get_event_list(tickers, start, interval):
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


def backtest(bots, tickers, start, interval):
    # Get price changes of all stocks sorted by time
    event_list = get_event_list(tickers, start, interval)
    # Loop over each event and let each bot handle it
    for event in event_list:
        for bot in bots:
            bot.handle_event(event)
    # Save all the different bot.actions in a dictionary
    actions = dict()
    for bot in bots:
        actions[bot.name] = bot.actions
    return actions


def test_algorithms(tickers, start, interval, bot_names, algorithm_name):

    # Load all bots that are selected in the workspace
    bots = [load_agent(name)() for name in bot_names]
    # Get dictionary of the actions that each bot made, where the bot name is the key
    actions = backtest(bots, tickers, start, interval)

    results = defaultdict(pd.DataFrame)

    for bot in bots:
        all_bot_actions = pd.DataFrame(columns=['Price', 'Position', 'Ticker'])
        for (timestamp, ticker, price), position in actions[bot.name]:
            _df = pd.DataFrame([[price, position, ticker]], columns=['Price', 'Position', 'Ticker'], index=[timestamp])
            all_bot_actions = all_bot_actions.append(_df)
        results[bot.name] = all_bot_actions
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

    percentual_profits = defaultdict(pd.DataFrame)
    for bot_name, bot_df in results.items():
        df = pd.DataFrame(columns=['Multiplier'])
        for ticker in bot_df.Ticker.unique():
            ticker_df = bot_df.loc[bot_df['Ticker'] == ticker]
            prices = ticker_df['Price']
            percentual_profit = 1
            for shift, (price, position) in enumerate(zip(prices[:-1], ticker_df['Position']), start=1):
                percentual_profit *= prices[shift]/price if position == 'long' else price/prices[shift]
            df.loc[ticker] = percentual_profit
        percentual_profits[bot_name] = df

    return percentual_profits


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