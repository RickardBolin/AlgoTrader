import file_system.trading_algorithms.Efficient_frontier.bot as ef
import file_system.trading_algorithms.universal_portfolio_bot.bot as up
import backend.algorithm as algo

tickers = ['ERIC-B.ST',
        'HM-B.ST',
        'ASSA-B.ST',
        'SHB-B.ST'
        ]
bots = [ef.Bot(tickers)]
algo.test_portfolios(bots, interval='1d', start='2017-07-16', end=None)


