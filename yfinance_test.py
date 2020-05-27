import yfinance as yf
import pandas
import matplotlib.pyplot as plt

msft = yf.Ticker("MSFT")
#print(msft)

"""
returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
#print(msft.info)

"""
returns:
{
 'quoteType': 'EQUITY',
 'quoteSourceName': 'Nasdaq Real Time Price',
 'currency': 'USD',
 'shortName': 'Microsoft Corporation',
 'exchangeTimezoneName': 'America/New_York',
  ...
 'symbol': 'MSFT'
}
"""

# get historical market data, here max is 5 years.
h = msft.history(period="1mo")
temp = h.get("High")
print(temp)
print(temp.get(0))

price = [temp.get(x) for x in range(10)]
x = [x for x in range(10)]
plt.plot(x,price)
plt.show()

"""
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-11-12  146.28  147.57  146.06  147.07    18641600        0.0     0.0
2019-11-13  146.74  147.46  146.30  147.31    16295622        0.0     0.0
"""

#tickers = yf.Tickers('msft aapl goog')


