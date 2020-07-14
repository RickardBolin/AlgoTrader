import pandas as pd
import numpy as np
from scipy.stats import norm
from backend.stochastic_processes.timeseries import pct_change
from backend.stochastic_processes.statistics import cov, mean


def VaR(df, weights, investment=None, percentile=5, days=1, decimal_points=2):
    """
    Value-at-Risk
    :param df:
    :param weights:
    :param investment:
    :param percentile:
    :param days:
    :return:
    """
    returns = pct_change(df, shift=1).dropna()
    avg_returns = mean(returns)
    cov_matrix = cov(returns)
    mu, sigma = avg_returns @ weights, np.sqrt(weights.T @ cov_matrix @ weights)

    if investment:
        mu, sigma = (1+mu)*investment, sigma*investment

    _var = norm.ppf(percentile/100, mu, sigma)

    if investment:
        _var = investment - _var
        _vars = [np.round(_var * np.sqrt(day), decimal_points) for day in range(1, days+1)]
        _vars = pd.DataFrame(_vars, columns=['VaR (Absolute)'], index=range(1, days + 1))
    else:
        _vars = [100*np.round(-1*_var * np.sqrt(day), decimal_points + 2) for day in range(1, days+1)]
        _vars = pd.DataFrame(_vars, columns=['VaR (Relative %)'], index=range(1, days + 1))

    return _vars
