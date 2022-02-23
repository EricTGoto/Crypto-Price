from dotenv import load_dotenv
load_dotenv()

import send_email

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json

token = os.environ.get("api-token")
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'id':'1027'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': token,
}

xd = {'status': {'timestamp': '2022-02-12T21:10:12.925Z', 'error_code': 0, 'error_message': None, 'elapsed': 33, 'credit_count': 1, 'notice': None}, 
      'data': {'1027': {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'num_market_pairs': 5495, 'date_added': '2015-08-07T00:00:00.000Z', 
      'tags': ['mineable', 'pow', 'smart-contracts', 'ethereum-ecosystem', 'binance-smart-chain', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 
      'polychain-capital-portfolio', 'binance-labs-portfolio', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 
      'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures-portfolio', 'hashkey-capital-portfolio', 
      'kenetic-capital-portfolio', 'huobi-capital-portfolio', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital-portfolio', 
      'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-portfolio'],
      'max_supply': None, 'circulating_supply': 119554055.999, 'total_supply': 119554055.999, 'is_active': 1, 'platform': None, 'cmc_rank': 2, 'is_fiat': 0, 
      'self_reported_circulating_supply': None, 'self_reported_market_cap': None, 'last_updated': '2022-02-12T21:08:00.000Z', 
      'quote': {'USD': {'price': 2964.9960961372876, 'volume_24h': 11739215450.346893, 'volume_change_24h': -24.4984, 'percent_change_1h': 0.37518614, 
      'percent_change_24h': 1.33554516, 'percent_change_7d': -1.61789835, 'percent_change_30d': -9.31483632, 'percent_change_60d': -21.4726274,
       'percent_change_90d': -34.74558589, 'market_cap': 354477309314.4137, 'market_cap_dominance': 18.52, 'fully_diluted_market_cap': 354477309314.41, 
       'last_updated': '2022-02-12T21:08:00.000Z'}}}}}

# print(xd['data']['1027']['name'])

session = Session()
session.headers.update(headers)
def getData():
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e) 

def extractInfo(data: dict, id: str):
  name = data['data'][id]['name']
  price = data['data'][id]['quote']['USD']['price']
  return [name, str(price)]

if __name__ == "__main__":
  data = getData()
  info = extractInfo(xd, '1027')
  sender = os.environ.get("test_sender")
  receiver = os.environ.get("test_receiver")
  service = send_email.create_service()
  message = send_email.create_message(sender, receiver, "Ethereum Update", " ".join(info) )
  return_msg = send_email.send_message(service, "me", message)
  print(return_msg)