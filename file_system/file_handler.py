import csv
import sys
from collections import defaultdict, namedtuple
sys.path.append('..')
from backend.utils import *
import pandas as pd


def read_result(file):
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
    with open(file, 'w') as f:
        f.write(str(len(results)) + '\n')

    for bot_name, df in results.items():
        with open(file, 'a') as f:
            f.write(bot_name + ',' + str(len(df.index)) + '\n')
            df.to_csv(f, index=True)




"""
def read_result(file):
    results = defaultdict(tuple)
    result_tuple = namedtuple('Results', ['timestamps', 'prices', 'positions'])
    with open(file) as _file:
        csv_reader = csv.reader(_file)
        num_bots, num_tickers = next(csv_reader)

        for bot_idx in range(int(num_bots)):

            bot_name = next(csv_reader)
            timestamps = defaultdict(list)
            prices = defaultdict(list)
            positions = defaultdict(list)

            for ticker_idx in range(int(num_tickers)):
                ticker, num_actions = next(csv_reader)
                for action_idx in range(int(num_actions)):
                    timestamp, price, position = next(csv_reader)
                    timestamps[ticker].append(timestamp)#convert_unix_to_timestamp(int(unix_time)))
                    prices[ticker].append(float(price))
                    positions[ticker].append(position)

            results[bot_name[0]] = result_tuple(timestamps, prices, positions)

    return results


def write_result(file, result):
    with open(file, 'w') as _file:
        csv_writer = csv.writer(_file)

        num_bots = len(result.keys())
        num_tickers = len(result[list(result.keys())[0]].positions)
        csv_writer.writerow([num_bots, num_tickers])
        for bot_name, (timestamps, prices, positions) in result.items():
            tickers = timestamps.keys()
            csv_writer.writerow([bot_name])
            for ticker in tickers:
                num_actions = len(timestamps[ticker])
                csv_writer.writerow([ticker, num_actions])
                for timestamp, price, position in zip(timestamps[ticker], prices[ticker], positions[ticker]):
                    csv_writer.writerow([timestamp, price, position])
"""