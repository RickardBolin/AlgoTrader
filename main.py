import requests
import json

url = 'https://api.worldtradingdata.com/api/v1/stock'
params = {
  'symbol': 'AAPL',
  'api_token': 'UoEbkafW25hRc6aVKZjkQvtabMa8kqyarF6gJkhy29MrzuRJVy1SOImjFom7'
}
response = requests.request('GET', url, params=params)

print(response.json())
