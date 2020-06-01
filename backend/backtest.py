from time import mktime
from datetime import datetime

from backend import stock_data as sd
import numpy as np


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


# INTE TESTAD!
def convert_timestamp_to_unix(timestamp):
    date = datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')
    return int(mktime(date.timetuple()))


# INTE TESTAD!
def convert_unix_to_timestamp(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def get_event_list(tickers, start="2016-05-25", interval="1d"):
    event_list = []
    ## First draft, måste göras snabbare!
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        for timestamp, new_price in stock_data["Close"].iteritems():
            unix_time = convert_timestamp_to_unix(timestamp)
            event_list.append([unix_time, ticker, new_price])
    event_list.sort(key=lambda x: x[0])
    return event_list
