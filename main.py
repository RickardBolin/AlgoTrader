import requests
import json

url = 'https://api.worldtradingdata.com/api/v1/stock'
params = {
  'symbol': 'SNAP,TWTR',
  'api_token': 'demo'
}
response = requests.request('GET', url, params=params)

print(response.json())
