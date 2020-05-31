from time import mktime
from datetime import datetime

from backend import stock_data as sd
import numpy as np


def backtest(algorithm, tickers):
    event_list = get_event_list(tickers)

    for event in event_list:
        algorithm.handle_event(event)

# INTE TESTAD!
def convert_timestamp_to_unix(timestamp):
    date = datetime.strptime(timestamp, '%Y-%m-%d')
    return int(mktime(date.timetuple()))


def convert_unix_to_timestamp(unix_time):
    return 0


def get_event_list(tickers, start="2016-05-25", interval="1d"):
    event_list = []
    ## First draft, måste göras snabbare!
    for ticker in tickers:
        stock_data = sd.get_stock_data(ticker, start=start, interval=interval)
        for event in stock_data:
            timestamp = event["Date"]
            new_price = event["Adj Close"]
            unix_time = convert_timestamp_to_unix(timestamp)
            event_list.append([unix_time, ticker, new_price])
    event_list.sort(key=lambda i: event_list[0])
    return event_list
