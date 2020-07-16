from file_system.trading_algorithms.Efficient_frontier.bot import Bot
import backend.algorithm as algo

tickers = ['ERIC-B.ST',
        'HM-B.ST',
        'ASSA-B.ST',
        'SHB-B.ST',
        'AAK.ST',
        'ABB.ST',
        'ADDT-B.ST',
        'AF-B.ST',
        'ALFA.ST',
        'ALIV-SDB.ST',
        ]
bots = [Bot(tickers)]
algo.test_portfolios(bots, interval='1d', start=None, end=None)


