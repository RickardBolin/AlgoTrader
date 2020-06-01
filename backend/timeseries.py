import numpy as np


def moving_average(data, window, rule='same'):
    #return np.nan_to_num(np.convolve(data, np.ones(window), rule) / window)
    return np.convolve(data, np.ones(window), rule) / window


def percentual_change(stock_data):
    one_day_ahead_stock_data = stock_data.shift(-1)
    percent_change = 100 * (one_day_ahead_stock_data - stock_data).div(stock_data)
    percent_change = percent_change.dropna()
    return percent_change