from collections import deque, defaultdict
import pandas as pd
import statsmodels.tsa.arima_model as arima_model


class Bot:
    """
    Just a test if statmodels is a good resource. Turns out to be so and we should build a framework to use it
    for training time series data.
    """
    def __init__(self):
        self.name = 'Dig bick'
        self.ARMA = defaultdict(arima_model.ARMAResults)
        self.train_data = defaultdict(pd.DataFrame)
        self.train_dps = 100
        self.seen_commodities = []
        self.actions = []
        self.pos = ''

    def handle_event(self, event):
        _time, com, price = event
        if com not in self.seen_commodities:
            self.seen_commodities.append(com)
            self.train_data[com] = pd.DataFrame(columns=['price'])

        num_dps = len(self.train_data[com])
        if num_dps < self.train_dps:
            self.train_data[com].loc[_time] = price
        elif num_dps == self.train_dps:
            _new_ARMA = arima_model.ARMA(self.train_data[com], (1, 1))
            new_ARMA = _new_ARMA.fit()
            new_ARMA.summary()
            self.ARMA[com] = new_ARMA
            self.train_data[com].loc[_time] = price
        else:
            self.algorithm(com, price, event)

    def algorithm(self, com, price, event):
        if self.pos != 'long':
            if price < self.ARMA[com].predict()[0]:
                self.pos = 'long'
                self.actions.append([event, 'long'])
        else:
            if price > self.ARMA[com].predict()[0]:
                self.pos = 'short'
                self.actions.append([event, 'short'])
