import numpy as np
from scipy import fft, ifft
import pandas as pd


def fourier_transform(df):
    """
    Calculates the fourier transform of some incoming data.
    :param data: Signal to be transformed.
    :return: Fourier transformed signal.
    """
    if isinstance(df, pd.Series):
        return pd.DataFrame(np.abs(fft(df)), columns=[df.name])

    fft_df = pd.DataFrame(columns=df.columns)
    for name, col in df.iteritems():
        fft_df[name] = np.abs(fft(col))
    return fft_df


def inverse_fourier_transform(df):
    """
    Calculates the inverse fourier transform of some incoming data.
    :param data: Signal to be inverse transformed.
    :return: Inversed fourier transformed signal.
    """
    if isinstance(df, pd.Series):
        return pd.DataFrame([np.abs(fft(df))], columns=[df.name])

    ifft_df = pd.DataFrame(columns=df.columns)
    for name, col in df.iteritems():
        ifft_df[name] = ifft(df)
    return ifft_df


def moving_average(df, window=10, rule='same'):
    """
    Computes a moving average of the data.
    :param data: Data to be averaged.
    :param window: Window size (Degree of the moving average).
    :param rule: ?
    :return: Moving average of prescribed data.
    """

    if isinstance(df, pd.Series):
        return pd.DataFrame(np.convolve(df, np.ones(window), rule) / window, index=df.index, columns=[df.name])

    ma_df = pd.DataFrame(columns=df.columns)
    for name, col in df.iteritems():
        ma_df[name] = np.convolve(col, np.ones(window), rule) / window

    return ma_df


def differencing(df, shift=1):
    """
    Differencing the data, i.e. (P_{i+shift} - P_{i}) for all i.
    :param data: The stock data to be transformed. Type sensitive! Must be pandas dataframe.
    :param shift: How large shift
    :return: Percentual change dataframe.
    """
    if not shift:
        shift = 1
    return df.shift(shift) - df


def pct_change(df, shift=1):
    """
    Calculates percentual change of the stock data, i.e. (P_{i+shift} - P_{i})/P_{i} for all i.
    :param data: The stock data to be transformed. Type sensitive! Must be pandas dataframe.
    :param shift: How large shift
    :return: Percentual change dataframe.
    """
    if not shift:
        shift = 1
    return df.pct_change(periods=shift)
