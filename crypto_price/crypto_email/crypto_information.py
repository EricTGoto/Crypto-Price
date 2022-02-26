from dotenv import load_dotenv
load_dotenv()

#import send_email

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json

class GetCryptoData():
    # map is one credit
    BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'
    TOKEN = os.environ.get("api-token")
    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': TOKEN,
    }

    def getData(self):
        url = GetCryptoData.BASE_URL + '/quotes/latest'
        parameters = {
            'id':'1027'
        }
        session = Session()
        session.headers.update(GetCryptoData.HEADERS)

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

    def getTopCoins(self, number_of_coins: int):
        """
        Gets the specified number of coins and returns the JSON response.
        """
        url = GetCryptoData.BASE_URL + "map"
        parameters = {
            'limit': number_of_coins,
            'sort': "cmc_rank"
        }
        session = Session()
        session.headers.update(GetCryptoData.HEADERS)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e) 

    def cleanMapResponse(self, data: dict) -> dict:
        """
        Takes in the dictionary result from the map api call and returns a formatted list of dictionaries with coin data.
        """
        formatted_data = []
        for coin in data['data']:
            formatted_data.append({
                'name': coin['name'],
                'symbol': coin['symbol'],
                'rank': coin['rank']
                })
        return formatted_data
        

if __name__ == "__main__":
    crypto_info = GetCryptoData()
    data = crypto_info.getTopCoins(5)
    #print(data)

    map_result = {'status': {'timestamp': '2022-02-26T18:31:54.293Z', 'error_code': 0, 'error_message': None, 'elapsed': 7, 'credit_count': 1, 'notice': None},
    'data': [
    {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'rank': 1, 'is_active': 1, 'first_historical_data': '2013-04-28T18:47:21.000Z', 'last_historical_data': '2022-02-26T18:29:00.000Z', 'platform': None}, 
    {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'rank': 2, 'is_active': 1, 'first_historical_data': '2015-08-07T14:49:30.000Z', 'last_historical_data': '2022-02-26T18:29:00.000Z', 'platform': None}, 
    {'id': 825, 'name': 'Tether', 'symbol': 'USDT', 'slug': 'tether', 'rank': 3, 'is_active': 1, 'first_historical_data': '2015-02-25T13:34:26.000Z', 'last_historical_data': '2022-02-26T18:29:00.000Z', 'platform':
    {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'token_address': '0xdac17f958d2ee523a2206206994597c13d831ec7'}},
    {'id': 1839, 'name': 'BNB', 'symbol': 'BNB', 'slug': 'bnb', 'rank': 4, 'is_active': 1, 'first_historical_data': '2017-07-25T04:30:05.000Z', 'last_historical_data': '2022-02-26T18:29:00.000Z', 'platform': None}, 
    {'id': 3408, 'name': 'USD Coin', 'symbol': 'USDC', 'slug': 'usd-coin', 'rank': 5, 'is_active': 1, 'first_historical_data': '2018-10-08T18:49:28.000Z', 'last_historical_data': '2022-02-26T18:29:00.000Z', 'platform': {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'slug': 'ethereum', 'token_address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'}}
    ]}

    print(crypto_info.cleanMapResponse(data))
    
    # info = extractInfo(xd, '1027')
    # sender = os.environ.get("test_sender")
    # receiver = os.environ.get("test_receiver")
    # service = send_email.create_service()
    # message = send_email.create_message(sender, receiver, "Ethereum Update", " ".join(info) )
    # return_msg = send_email.send_message(service, "me", message)
    # print(return_msg)