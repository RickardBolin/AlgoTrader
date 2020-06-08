from collections import defaultdict
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
        self.forecast_idx = 0
        self.seen_commodities = []
        self.actions = []
        self.pos = ''

    def handle_event(self, event):
        _time, com, price = event
        if com not in self.seen_commodities:
            self.seen_commodities.append(com)
            self.train_data[com] = pd.DataFrame(columns=['price'])

        self.train_data[com].loc[_time] = price

        num_dps = len(self.train_data[com])
        if num_dps < self.train_dps:
            pass

        elif num_dps % self.train_dps == 0:
            _new_ARMA = arima_model.ARMA(self.train_data[com], (1, 1))
            new_ARMA = _new_ARMA.fit()
            self.ARMA[com] = new_ARMA
            self.predictions = self.ARMA[com].predict(0, self.train_dps)
            self.forecast_idx = 0
        else:
            self.algorithm(price, event)

    def algorithm(self, price, event):
        if self.pos != 'long':
            if price < self.predictions[self.forecast_idx]:
                self.pos = 'long'
                self.actions.append([event, 'long'])
        else:
            if price > self.predictions[self.forecast_idx]:
                self.pos = 'short'
                self.actions.append([event, 'short'])
        self.forecast_idx += 1
