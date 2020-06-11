import numpy as np
import pandas as pd

"""
File that shall be filled with functions related to Stochastic Differential Equations.

Could be relevant:
https://github.com/mattja/sdeint/tree/master/sdeint
"""


def brownian_motion(steps):
    """
    Calculates a
    :param steps:
    :return:
    """
    dt = 1./steps
    b = np.random.normal(0, np.sqrt(dt), steps)
    W = np.cumsum(b)
    return W


def gbm(start_price, avg_return, vol, steps, bm=None):

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
    if not bm:
        bm = brownian_motion(steps)
    stock_price = np.zeros(steps)
    mu, sigma = avg_return * steps, vol * np.sqrt(steps)

    for step in range(steps):

        drift = (mu - 0.5 * (sigma ** 2)) * t[step]
        diffusion = sigma * bm[step]
        stock_price[step] = start_price * np.exp(drift + diffusion)

    return stock_price


def ornstein_uhlenbeck(start_price, avg_return, vol, steps, theta=0):
    """
    Solver to the SDE:

    dS_t = theta * (mean - S_t) * dt + std * dB_t

    method: Euler-Maruyama -> S_t = S_{t-1} + a(S_{t-1}) dt + b(S_{t-1}) dB_{t-1}

    :param start_price: Initial stock price.
    :param avg_return: Expected average return
    :param vol: Expected (average) volatility
    :param steps: Length of process.
    :param theta: Optional scaling term for the drift (optional).
    :return: Estimated future returns based on the Ornstein-Uhlenbeck SDE.
    """

    # t = t(start, end, steps), dt = t[1:] - t[:-1]. But we always have unit step so dt = 1.
    dt = 1
    bm = brownian_motion(steps)
    dB = bm[1:] - bm[:-1]
    returns = np.zeros(steps)
    returns[0] = start_price
    for step in range(1, steps):
        returns[step] = returns[step-1] + theta * (avg_return - returns[step-1]) * dt + vol * dB[step-1]
    return returns


def runge_kutta():
    """
    Might be added later.
    """
    pass
