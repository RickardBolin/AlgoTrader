import numpy as np


def moving_average(data, window, rule='same'):
    """
    Computes a moving average of the data.
    :param data: Data to be averaged.
    :param window: Window size (Degree of the moving average).
    :param rule: ?
    :return: Moving average of prescribed data.
    """
    return np.convolve(data, np.ones(window), rule) / window


def percentual_change(stock_data, shift):
    """
    Calculates percentual change of the stock data, i.e. (P_{i+shift} - P_{i})/P_{i} for all i.
    :param stock_data: The stock data to be transformed. Type sensitive! Must be pandas dataframe.
    :param shift: How large shift
    :return: Percentual change dataframe.
    """
    if not shift:
        shift = 1
    one_day_ahead_stock_data = stock_data.shift(-1*shift)
    percent_change = 100 * (one_day_ahead_stock_data - stock_data).div(stock_data)
    #percent_change = percent_change.dropna()
    return percent_change
