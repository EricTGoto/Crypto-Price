from dotenv import load_dotenv
load_dotenv()

#import send_email

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json

class GetCryptoData():

  def getData(self):
    token = os.environ.get("api-token")
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'id':'1027'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': token,
    }
    session = Session()
    session.headers.update(headers)
    
    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e) 

  def extractInfo(self, data: dict, id: str):
    name = data['data'][id]['name']
    price = data['data'][id]['quote']['USD']['price']
    return [{'name': name, 'price': price}]

if __name__ == "__main__":
  crypto_info = GetCryptoData()
  data = crypto_info.getData()
  print(data)
  # info = extractInfo(xd, '1027')
  # sender = os.environ.get("test_sender")
  # receiver = os.environ.get("test_receiver")
  # service = send_email.create_service()
  # message = send_email.create_message(sender, receiver, "Ethereum Update", " ".join(info) )
  # return_msg = send_email.send_message(service, "me", message)
  # print(return_msg)