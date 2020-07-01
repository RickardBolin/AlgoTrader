import backend.portfolio_management.efficient_frontier as ef
import backend.portfolio_management.risk as risk
import backend.data_handler.stock_data as sd

df = sd.get_stock_data(['AAPL', 'TSLA', 'FLWS'])
df = df['Close']

_ef = ef.EfficientFrontier(df)

w = _ef.opts_by_sr[1]

print(risk.VaR(df, weights=w, investment=100000,days=15))
print(risk.VaR(df, weights=w, days=15))