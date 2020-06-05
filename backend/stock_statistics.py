import pandas as pd
import numpy as np


def calc_stock_statistics(stock_data):

    cols = ['Average price', 'Standard deviation of price', 'Average returns', 'Standard deviation of returns']

    if isinstance(stock_data, pd.Series):
        return pd.DataFrame([_basic_statistics(stock_data)], columns=cols, index=[stock_data.name]), \
                pd.DataFrame([1], columns=[stock_data.name], index=[stock_data.name])

    tickers = stock_data.columns
    statistics_df = pd.DataFrame(columns=cols)
    for ticker in tickers:
        statistics_df.loc[ticker] = _basic_statistics(stock_data[ticker])

    return statistics_df, stock_data.corr()


def _basic_statistics(df):
    returns = (df.shift(-1) - df).div(df)
    returns = returns.dropna()
    return df.mean(), df.std(), returns.mean(), returns.std()
