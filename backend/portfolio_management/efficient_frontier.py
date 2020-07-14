from copy import copy
import numpy as np
import pandas as pd
from backend.stochastic_processes.statistics import mean, cov
from backend.stochastic_processes.timeseries import pct_change


class EfficientFrontier:
    """
    A class which finds the optimal commodity allocation from a dataframe of commidities with history of prices.
    Used for risk management. Not relevent for algorithmic trading but suitable for riskmanagement (hedgeing).
    """
    def __init__(self, df, rf=0.02, log=True, num_trade_days=252):
        """

        :param df:
        :param rf:
        :param log:
        :param num_trade_days:
        """
        # Prep
        self.num_trade_days = num_trade_days
        self.rf = rf
        self.stocks = [stock for stock in df.columns]
        self.returns = (np.log(df) - np.log(df.shift(1))).dropna() if log else pct_change(df, shift=1).dropna()
        self.expected_returns = ((1 + mean(self.returns)) ** 252) - 1

        self.return_covs = cov(self.returns * self.num_trade_days)
        _allocation = np.linalg.solve(self.return_covs, self.expected_returns - self.rf)
        self.p_allocation = _allocation/sum(_allocation)
        self.p_return = sum(alloc * exp_ret for alloc, exp_ret in zip(self.p_allocation, self.expected_returns))
        self.p_std = np.sqrt(self.p_allocation.T @ self.return_covs @ self.p_allocation)

    def return_allocation(self, target_return):
        wp = (target_return - self.rf)/(self.p_return - self.rf)
        _opt_alloc = wp*self.p_allocation
        cols = copy(self.stocks)
        cols.append('rf')
        _opt_alloc = np.append(_opt_alloc, 1-wp)
        return pd.DataFrame([_opt_alloc], columns=cols, index=[f'W for return={target_return}'])

    def risk_allocation(self, target_risk):
        wp = (target_risk/self.p_std)
        _opt_alloc = wp*self.p_allocation
        cols = copy(self.stocks)
        cols.append('rf')
        _opt_alloc = np.append(_opt_alloc, 1-wp)
        return pd.DataFrame([_opt_alloc], columns=cols, index=[f'W for vol={target_risk}'])
