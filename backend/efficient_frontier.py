import matplotlib.pyplot as plt
import numpy as np
import backend.stock_data as sd


class EfficientFrontier:

    def __init__(self, df):
        # Prep
        self.num_trade_days = 252
        self.num_simulations = 10000
        self.num_stocks = len(df.columns)
        self.log_returns = np.log(df) - np.log(df.shift(1))
        self.return_means = self.log_returns.mean()
        self.return_covs = self.log_returns.cov()
        # Solve
        self.returns, self.stds, self.sharpe_ratios, self.all_weights = self._simulate()
        self.opts_by_sr = self.maximize_sr()
        self.opts_by_std = self.minimize_std()
        self.opts_by_return = self.maximize_return()
        self.plot()

    def plot(self):
        fig, ax = plt.subplots()
        plt.scatter(x=self.stds, y=self.returns, c=self.sharpe_ratios, cmap='viridis')
        plt.colorbar(label='Sharpe Ratio')
        opts = [self.opts_by_sr, self.opts_by_std, self.opts_by_return]
        colors = ['g', 'r', 'k']
        labels = ['Maximized sr: sr = ', 'Minimized std: sr = ', 'Maximized return: sr = ']
        for opt, color, label in zip(opts, colors, labels):
            ax.scatter(opt[2][0], opt[2][1], marker='*', c=color, s=100, label=label + str(f'{opt[0]:.2f}'))
        ax.legend()
        plt.xlabel('Volatility')
        plt.ylabel('Log-returns')
        plt.title('Efficient frontier')
        plt.show()

        plt.show()

    def _simulate(self):
        returns = np.zeros(self.num_simulations)
        stds = np.zeros(self.num_simulations)
        sharpe_ratios = np.zeros(self.num_simulations)
        all_weights = np.zeros((self.num_simulations, self.num_stocks))

        for simulation in range(self.num_simulations):
            weights = np.random.rand(self.num_stocks)
            weights /= np.sum(weights)

            all_weights[simulation, :] = weights
            returns[simulation] = np.sum(self.return_means * weights * self.num_trade_days)
            stds[simulation] = np.sqrt(weights @ self.return_covs @ weights.T)
            sharpe_ratios[simulation] = returns[simulation]/stds[simulation]

        return returns, stds, sharpe_ratios, all_weights

    @staticmethod
    def _find_max(array):
        return array.max(), array.argmax()

    @staticmethod
    def _find_min(array):
        return array.min(), array.argmin()

    def maximize_sr(self):
        max_sr, argmax_sr = self._find_max(self.sharpe_ratios)
        opt_weights = self.all_weights[argmax_sr, :]
        opt_point = (self.stds[argmax_sr], self.returns[argmax_sr])
        return max_sr, opt_weights, opt_point

    def minimize_std(self):
        min_std, argmin_std = self._find_min(self.stds)
        opt_point = (self.stds[argmin_std], self.returns[argmin_std])
        opt_weights = self.all_weights[argmin_std, :]
        return opt_point[1]/opt_point[0], opt_weights, opt_point

    def maximize_return(self):
        max_return, argmax_return = self._find_max(self.returns)
        opt_point = (self.stds[argmax_return], self.returns[argmax_return])
        opt_weights = self.all_weights[argmax_return, :]
        return opt_point[1] / opt_point[0], opt_weights, opt_point


# Test
df = sd.get_stock_data(['AAPL', 'TSLA', 'FLWS'])
df = df['Close']
ef = EfficientFrontier(df=df)

