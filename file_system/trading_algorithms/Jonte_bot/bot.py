import pandas as pd
import numpy as np
class Bot:
    def __init__(self):
        self.name = "Jonte_bot"
        self.scale = 184.83719635009766
        self.shift = 76.8767318725586
        self.df_main = pd.DataFrame(columns=['Main'])
        self.df_tickers = [0,0,0,0,0,0,0,0]
        self.df_close = [0,0,0,0,0,0,0,0]
        self.df = pd.DataFrame(columns=['Main, 1, 2 ,3 ,4 ,5 ,6 ,7, ma7, ma21, ema26, ema12, MACD, std20, upper_band, lower_band, ema, momentum, fft3, fft6,fft9'])
        self.i = 0
        self.tickers = {}
        self.actions = []
        self.time = 0
        self.main_ticker = ''


    def handle_event(self, event):
        timestamp, ticker, new_close = event
        if self.i == 0:
            self.main_ticker = ticker
        if self.time < 100 and ticker == self.main_ticker:
            self.df_main.append([new_close])
            self.time += 1
            print(self.time)
        if self.time >= 100:
            print(self.df_main.head())
            self.data_proc(ticker,new_close)

    def algorithm(self, event):
        pass

    def data_proc(self,ticker, price):
        if sum(self.df_close) == 8:
            print(self.df_tickers[0])
            self.df_main.append([self.df_tickers[0]])
            ma7 = self.df_main.rolling(window=7).mean()['Main'].tolist()
            ma21 = self.df_main.rolling(window=21).mean()
            ema26 = self.df_main.ewm(span=26).mean()
            ema12 = self.df_main.ewm(span=12).mean()
            MACD = ema12-ema26
            std20 = self.df_main.rolling(20).std()
            upper_band = ma21 + std20*2
            lower_band = ma21 -std20*2
            ema = self.df_main.ewm(com=0.5).mean()
            momentum = self.df_main.pct_change()

            close_fft = np.fft.fft(np.asarray(self.df_main.to_numpy()))
            fft_list = np.copy(close_fft)
            fft_list[3:-3] = 0
            fft3 = abs(np.fft.ifft(fft_list))
            fft_list = np.copy(close_fft)
            fft_list[6:-6] = 0
            fft6 = abs(np.fft.ifft(fft_list))
            fft_list = np.copy(close_fft)
            fft_list[9:-9] = 0
            fft9 = abs(np.fft.ifft(fft_list))

            self.df_tickers.extend([ma7, ma21, ema26, ema12, MACD, std20, upper_band, lower_band, ema, momentum, fft3, fft6,fft9])
            test = [(x-self.shift)/self.scale for x in self.df_tickers]

            self.df.append(test)
            self.df_close = [0,0,0,0,0,0,0,0]

            index = self.tickers_to_index(ticker)
            self.df_close[index] = 1
            self.df_tickers[index] = price
            print(self.df.head())
        else:
            index = self.tickers_to_index(ticker)
            self.df_close[index] = 1
            self.df_tickers[index] = price


    def tickers_to_index(self,ticker):
        if ticker not in self.tickers:
            self.tickers[ticker] = self.i
            self.i += 1
            return self.i-1
        else:
            return self.tickers[ticker]
