import pandas as pd


def calc_stock_statistics(stock_data):
    """FIXA OM BARA EN VARIABEL, ISF ÄR SERIES OBJ."""

    tickers = stock_data.columns
    statistics_df = pd.DataFrame(columns=['Mean', 'Vol'])
    for ticker in tickers:
        statistics_df.loc[ticker] = _basic_statistics(stock_data[ticker])

    return statistics_df, stock_data.corr()


def _basic_statistics(df):
    return df.mean(), df.std()
