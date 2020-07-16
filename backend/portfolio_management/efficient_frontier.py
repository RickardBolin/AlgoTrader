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
    """
    FIXA DENNA NGT ÄR SKEVT!!!!
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
        self.log = log
        self.prev_prices = df.tail(1).iloc[0]
        self.stocks = [stock for stock in df.columns]

        self.returns = (np.log(df) - np.log(df.shift(1))).dropna()
        self.expected_returns = (1 + mean(self.returns)) ** self.num_trade_days - 1
        self.expected_cov_m = cov(self.returns) * self.num_trade_days

        self.solve()

    def solve(self):
        _allocation = np.linalg.solve(self.expected_cov_m, self.expected_returns)
        self.p_allocation = _allocation / sum(_allocation)
        self.p_return = sum(alloc * exp_ret for alloc, exp_ret in zip(self.p_allocation, self.expected_returns))
        self.p_std = np.sqrt(self.p_allocation.T @ self.expected_cov_m @ self.p_allocation)

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

    def update_window(self, row_to_add, recalculate_cov=False):
        # Fix log later
        _return = np.log(row_to_add) - np.log(self.prev_prices)
        e_return = (1 + _return) ** self.num_trade_days - 1

        self.expected_returns = (1/self.num_trade_days) * ((self.num_trade_days - 1) * self.expected_returns + e_return)

        self.returns.loc[row_to_add.name] = e_return
        self.returns.drop(self.returns.index[0], inplace=True)

        if recalculate_cov:
            self.expected_cov_m = cov(self.returns) * self.num_trade_days

        else:
            # ej klar
            pass

        self.prev_prices = row_to_add
        self.solve()
