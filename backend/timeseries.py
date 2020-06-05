import numpy as np
from scipy import fft, ifft
from scipy.signal import butter


def fourier_transform(data, none="None"):
    y = np.abs(fft(data))
    y[len(y)//2:] = 0
    return y#np.log(y)


def inverse_fourier_transform(data, none="None"):
    return ifft(data)


def moving_average(data, window, rule='same'):
    """
    Computes a moving average of the data.
    :param data: Data to be averaged.
    :param window: Window size (Degree of the moving average).
    :param rule: ?
    :return: Moving average of prescribed data.
    """
    y = np.convolve(data, np.ones(window), rule) / window
    y[:window] = y[-window:] = -float("Inf")
    return y


def percentual_change(data, shift):
    """
    Calculates percentual change of the stock data, i.e. (P_{i+shift} - P_{i})/P_{i} for all i.
    :param data: The stock data to be transformed. Type sensitive! Must be pandas dataframe.
    :param shift: How large shift
    :return: Percentual change dataframe.
    """
    if not shift:
        shift = 1
    return data.pct_change(periods=shift)
