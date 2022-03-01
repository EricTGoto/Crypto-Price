from dotenv import load_dotenv
load_dotenv()

#import send_email

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json
from math import floor

class GetCryptoData():
    # map and quotes/latest is one credit
    # 333 credits per day, 10000 a month
    BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'
    TOKEN = os.environ.get("api-token")
    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': TOKEN,
    }

    def get_data_from_cmp(self, id: list) -> dict:
        """
        Takes in a list of ids and gets the latest quote data.
        Note: data is returned in order of ascending IDs.
        """
        url = GetCryptoData.BASE_URL + 'quotes/latest'
        parameters = {
            'id': ','.join(map(str,id))
        }
        session = Session()
        session.headers.update(GetCryptoData.HEADERS)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e) 

    def extract_info(self, data: dict, id: str):
        name = data['data'][id]['name']
        price = data['data'][id]['quote']['USD']['price']
        return [{'name': name, 'price': price}]

    def get_top_coins(self, number_of_coins: int):
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

    def clean_map_response(self, map_response: dict) -> dict:
        """
        Takes in the dictionary result from the map api call and returns a formatted list of dictionaries with coin data.
        """
        formatted_data = []
        for coin in map_response['data']:
            formatted_data.append({
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'rank': coin['rank']
                })
        return formatted_data

    def get_IDs(self, map_response: dict):
        """
        Takes map response dictionary and extracts the IDs
        """    
        IDs = []
        for coin in map_response['data']:
            IDs.append(coin['id'])
        return IDs

    def add_coin_data_from_quotes_latest(self, quotes_latest_data: dict, cleaned_map_data: list):
        '''
        Takes in quotes latest data and cleaned map data and adds price info to the cleaned map data.
        Returns a list of dictionaries with the following keys:
        id, name, symbol, rank, price
        '''
        for id, info in quotes_latest_data['data'].items():
            for coin_data in cleaned_map_data:
                if coin_data['id'] == int(id):
                    coin_data['price'] = round(info['quote']['USD']['price'], 2)
                    coin_data['market_cap'] = floor(info['quote']['USD']['market_cap'])
                    coin_data['percent_change_24h'] = round(info['quote']['USD']['percent_change_24h'], 2)
                    coin_data['percent_change_90d'] = round(info['quote']['USD']['percent_change_90d'], 2)
                    break
        return cleaned_map_data

    def get_quotes(self, number_of_quotes: int):
        """
        Gets formatted data.
        """
        crypto_info = GetCryptoData()
        map_data = crypto_info.get_top_coins(number_of_quotes)
        data = crypto_info.clean_map_response(map_data)
        ids = crypto_info.get_IDs(map_data)
        quotes= crypto_info.get_data_from_cmp(ids)
        data = crypto_info.add_coin_data_from_quotes_latest(quotes, data)
        return data

if __name__ == "__main__":
    crypto_info = GetCryptoData()
    #data = crypto_info.get_top_coins(2)
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

    ids= crypto_info.get_IDs(map_result)
    quotes_latest_result = crypto_info.get_data_from_cmp(ids)
    clean = crypto_info.clean_map_response(map_result)
    print(quotes_latest_result)
    print(clean)
    print(crypto_info.add_coin_data_from_quotes_latest(quotes_latest_result, clean))
    
    # info = extractInfo(xd, '1027')
    # sender = os.environ.get("test_sender")
    # receiver = os.environ.get("test_receiver")
    # service = send_email.create_service()
    # message = send_email.create_message(sender, receiver, "Ethereum Update", " ".join(info) )
    # return_msg = send_email.send_message(service, "me", message)
    # print(return_msg)