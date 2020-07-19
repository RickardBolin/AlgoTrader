import backend.portfolio_management.efficient_frontier as ef
import backend.portfolio_management.risk as risk
import backend.data_handler.stock_data as sd

stocks = sd.get_stock_data(['AAPL', 'TSLA', 'FLWS'])
stocks = stocks['Close']

_ef = ef.EfficientFrontier(stocks)
alloc = _ef.p_allocation

print(risk.VaR(stocks, alloc, days=9))
print(risk.VaR(stocks, alloc, investment=100000, days=9))

