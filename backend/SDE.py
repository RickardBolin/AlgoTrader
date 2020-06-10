import numpy as np
import pandas as pd

"""
File that shall be filled with functions related to Stochastic Differential Equations.
"""


def brownian_motion(steps):
    """
    Calculates a
    :param steps:
    :return:
    """
    dt = 1./steps
    b = np.random.normal(0, 1, steps) * np.sqrt(dt)
    W = np.cumsum(b)
    return W


def gbm(start_price, avg_return, vol, steps):

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

    t = np.arange(steps)
    bm = brownian_motion(steps)
    returns = np.zeros(steps)
    for step in range(steps):
        drift = (avg_return - 0.5 * (vol ** 2)) * t[step]
        diffusion = vol * bm[step]
        returns[step] = start_price * np.exp(drift + diffusion)
    return returns


def euler_maruyama():
    pass
