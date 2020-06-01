import csv
import sys
from collections import defaultdict, namedtuple
from backend.utils import *
sys.path.append('..')

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
                    unix_time, price, position = next(csv_reader)
                    timestamps[ticker].append(convert_unix_to_timestamp(int(unix_time)))
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
                    csv_writer.writerow([convert_timestamp_to_unix(timestamp), price, position])
