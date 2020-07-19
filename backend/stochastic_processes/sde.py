import numpy as np
import pandas as pd
from abc import abstractmethod, ABC

"""
File that shall be filled with functions related to Stochastic Differential Equations.

Could be relevant:
https://github.com/mattja/sdeint/tree/master/sdeint
"""

"""
NÅGOT HÄR ÄR FISHY!
"""


class SDE(ABC):

    def __init__(self):
        pass

    @staticmethod
    def brownian_motion(length, num_bms=1):
        """
        Calculates a brownian motion.
        :param length: Length of brownian motion.
        :param num_bms: How many brownian motions to be simulated.
        :return: Matrix of brownian motion processes.
        """
        dt = 1.
        b = np.random.normal(0, np.sqrt(dt), (length, num_bms))
        W = np.cumsum(b, axis=0)
        return W

    @abstractmethod
    def integrate(self, *args):
        pass

    @abstractmethod
    def simulate(self, *args):
        pass


class GBM(SDE):

    def __init__(self, start_value, avg_returns, avg_vol, interval='D'):
        super(GBM, self).__init__()
        self.avg_returns = avg_returns
        self.avg_vols = avg_vol
        self.interval = interval

        self.start_time = 0
        self.start_price = start_value

    def integrate(self, steps, bm):
        t = np.arange(steps)
        expected_returns, expected_vols = self.avg_returns * steps, self.avg_vols * np.sqrt(steps)

        drift = (expected_returns - 0.5 * np.power(expected_vols, 2)) * t
        diffusion = expected_vols * bm
        stock_prices = self.start_price * np.exp(drift + diffusion)

        return stock_prices

    def simulate(self, steps, sims=1e5):
        simulations = np.zeros((steps, sims))
        sims = int(sims)
        bms = self.brownian_motion(steps, num_bms=sims).T
        for i, bm in enumerate(bms):
            simulations[:, i] = self.integrate(steps, bm=bm)

        return simulations


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
