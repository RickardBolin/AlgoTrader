import numpy as np
import pandas as pd
import google_docs_dev.features.statistics as stat
import google_docs_dev.features.timeseries as ts

"""
File that shall be filled with functions related to Stochastic Differential Equations.

Could be relevant:
https://github.com/mattja/sdeint/tree/master/sdeint
"""


def brownian_motion(length, num_bms=1):
    """
    Calculates a brownian motion.
    :param length: Length of brownian motion.
    :param num_bms: How many brownian motions to be simulated.
    :return: Matrix of brownian motion processes.
    """
    dt = 1./length
    b = np.random.normal(0, np.sqrt(dt), (length, num_bms))
    W = np.cumsum(b, axis=0)
    return W


def gbm(df, steps, expected_returns=None, expected_vols=None, bm=None, interval='D'):
    """
    GBM = geometric brownian motion, is the name of the standard stochastic differential equation for modeling
    stock prices:
    dS_t = mean(S_t) dt + std(S_t) dB_t
    Where S_t is the stock price and B_t is brownian motion.
    GBM has a closed form solution: S_t = S_0 * exp( (mean - var / 2) * t + std * B_t )

    Constructs a k-step prediction vector of the stock movement based on the Geometric brownian motion model.
    :param start_price: Initial stock price.
    :param avg_return: Expected average return
    :param vol: Expected (average) volatility
    :param steps: Length of process.
    :return: Estimated future returns based on the gbm SDE.
    """
    t = pd.date_range(df.index[-1], periods=steps+1, freq=interval).drop(df.index[-1])
    num_cols = df.shape[1]
    stock_prices = np.zeros((steps, num_cols))

    start_prices = df.tail(1)

    if not bm:
        bm = brownian_motion(steps, num_bms=num_cols)

    if not expected_returns:
        expected_returns = stat.mean(ts.differentiate(df, 1).dropna()) * steps

    if not expected_vols:
        expected_vols = stat.std(ts.differentiate(df, 1).dropna()) * np.sqrt(steps)

    for step in range(steps):
        drift = (expected_returns - 0.5 * np.power(expected_vols, 2)) * t[step]
        diffusion = expected_vols * bm[step]
        stock_prices[step] = start_prices * np.exp(drift + diffusion)

    return pd.DataFrame(stock_prices, columns=df.columns, index=t)


def ornstein_uhlenbeck(df, steps, theta=1, expected_returns=None, expected_vols=None, bm=None, interval='D'):
    """
    Solver to the SDE:

    dS_t = theta * (mu - S_t) * dt + sigma * dB_t

    method: Euler-Maruyama -> S_t = S_{t-1} + a(S_{t-1}) dt + b(S_{t-1}) dB_{t-1}

    :param start_price: Initial stock price.
    :param avg_return: Expected average return
    :param vol: Expected (average) volatility
    :param steps: Length of process.
    :param theta: Optional scaling term for the drift (optional).
    :return: Estimated future returns based on the Ornstein-Uhlenbeck SDE.
    """

    t = pd.date_range(df.index[-1], periods=steps + 1, freq=interval).drop(df.index[-1])
    num_cols = df.shape[1]
    stock_prices = np.zeros((steps, num_cols))
    start_prices = df.tail(1)

    if not bm:
        bm = brownian_motion(steps, num_bms=num_cols)

    if not expected_returns:
        expected_returns = stat.mean(ts.differentiate(df, 1).dropna()) * steps

    if not expected_vols:
        expected_vols = stat.std(ts.differentiate(df, 1).dropna()) * np.sqrt(steps)

    dt = 1
    dB = bm[1:] - bm[:-1]
    stock_prices[0] = start_prices
    for step in range(1, steps):
        stock_prices[step] = stock_prices[step-1] + theta * (expected_returns - stock_prices[step-1]) * dt + expected_vols * dB[step-1]

    return pd.DataFrame(stock_prices, columns=df.columns, index=t)


def runge_kutta():
    """
    Might be added later.
    """
    pass
