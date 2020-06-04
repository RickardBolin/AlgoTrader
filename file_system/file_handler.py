import csv
import sys
from collections import defaultdict
sys.path.append('..')
import pandas as pd


def read_result(file):
    """
    Reads file and construct a dictionary with (bot name, bot dataframe) as key-value pair.
    :param file: File to be read.
    :return: Result dictionary.
    """
    bots = defaultdict(pd.DataFrame)
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        num_bots = int(next(csv_reader)[0])
        bot_idx = 0
        while bot_idx < num_bots:
            bot_info = next(csv_reader)
            bot_name = bot_info[0]
            num_actions = int(bot_info[1])
            cols = next(csv_reader)[1:]
            df = pd.DataFrame(columns=cols)
            for action_idx in range(num_actions):
                timestamp, price, position, ticker = next(csv_reader)
                df = df.append(pd.DataFrame([[float(price), position, ticker]], columns=cols, index=[timestamp]))
            bots[bot_name] = df
            bot_idx += 1
    return bots


def write_result(file, results):
    """
    Writes results to a file. Results assumed to be a dictionary with (bot name, bot dataframe) as key-value pair.

    DATA STORAGE INFO: First row contains number of bots. Thereafter the following rows have the following structure:
    bot name, Number of actions.
    Dataframe columns: '', Price, Position, Ticker.
    action
    action
    ...
    action
    bot name, number of actions
    etc.

    :param file: filepath.
    :param results: Results to be written to file.
    """
    with open(file, 'w', newline='') as f:
        f.write(str(len(results)) + '\n')

    for bot_name, df in results.items():
        with open(file, 'a', newline='') as f:
            f.write(bot_name + ',' + str(len(df.index)) + '\n')
            df.to_csv(f, index=True)


def read_statistics(file):
    """
    Reads file and construct a dictionary with (bot name, bot dataframe) as key-value pair.
    :param file: File to be read.
    :return: Statistics dictionary.
    """
    bots = defaultdict(pd.DataFrame)
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        num_bots = int(next(csv_reader)[0])
        bot_idx = 0
        while bot_idx < num_bots:
            bot_info = next(csv_reader)
            bot_name = bot_info[0]
            num_tickers = int(bot_info[1])
            cols = next(csv_reader)[1:]
            df = pd.DataFrame(columns=cols)
            for ticker_idx in range(num_tickers):
                ticker, multiplier = next(csv_reader)
                df = df.append(pd.DataFrame([[f'{float(multiplier):.2f}']], columns=cols, index=[ticker]))
            bots[bot_name] = df
            bot_idx += 1
    return bots


def write_statistics(file, statistics):
    """
    Writes statistics to a file. Results assumed to be a dictionary with (bot name, bot dataframe) as key-value pair.

    DATA STORAGE INFO: First row contains number of bots. Thereafter the following rows have the following structure:
    bot name, number of tickers
    Dataframe columns: '', Multiplier
    ticker, multiplier
    ticker, multiplier
    ...
    ticker, multiplier
    bot name, number of tickers
    etc.

    :param file: filepath.
    :param statistics: statistics to be written to file.
    """
    with open(file, 'w', newline='') as f:
        f.write(str(len(statistics)) + '\n')

    for bot_name, df in statistics.items():
        with open(file, 'a', newline='') as f:
            f.write(bot_name + ',' + str(len(df.index)) + '\n')
            df.to_csv(f, index=True)
