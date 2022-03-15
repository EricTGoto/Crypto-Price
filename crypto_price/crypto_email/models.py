from asyncio.windows_events import NULL
from django.db import models
from django.utils import timezone
from .crypto_information import GetCryptoData
from crypto_tracker.models import Coin

class TopCrypto(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.IntegerField()
    percent_change_24h = models.DecimalField(max_digits=5, decimal_places=2)
    percent_change_90d = models.DecimalField(max_digits=5, decimal_places=2)
    symbol = models.CharField(max_length=5)
    rank = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    def fetch_data(self, number_of_coins: int):
        """
        Fetches data depending on the scenario.
        """
        # If database is empty, then fetch data from CoinMarketCap.
        if TopCrypto.objects.all().count() == 0:
            print("initial data fetch")
            data = self.initial_data_fetch(number_of_coins)
            self.download_new_icons(data)
            return data
        # If database is not empty and the stored data is more than x minutes old then fetch new data.
        elif (timezone.now() - TopCrypto.objects.first().time_stamp).seconds/60 >= 1:
            print("fetch new data")
            data = self.fetch_new_data(number_of_coins)
            self.download_new_icons(data)
            return data
        # If database is not empty and stored data is less than x minutes old, grab the stored data
        else:
            print("stored data")
            return TopCrypto.objects.all()
    
    def download_new_icons(self, data):
        icons_to_get = []
        for info in data:
            if Coin.objects.filter(name=info['name']).count() == 0: 
                icons_to_get.append(info['id'])
                Coin(name=info['name'], symbol=info['symbol']).save()
        print(f'got {len(icons_to_get)} icons')
        self.get_icons(icons_to_get)

    def get_icons(self, icon_list: list):
        crypto_info = GetCryptoData()
        icon_links = crypto_info.get_icon(icon_list)
        crypto_info.download_image(icon_links)

    def initial_data_fetch(self, number_of_coins: int):
        """
        When the website is accessed for the first time, the database will be empty so data will have to be fetched with the CMC API and then stored in to the database.
        """
        crypto_info = GetCryptoData()
        data = crypto_info.get_quotes(number_of_coins)

        # Store into database
        for coin in data:
            new_data = TopCrypto(name=coin['name'],price=coin['price'],market_cap=coin['market_cap'],percent_change_24h=coin['percent_change_24h'],percent_change_90d= coin['percent_change_90d'], symbol=coin['symbol'], rank=coin['rank'])
            new_data.save()

        return data

    def fetch_new_data(self, number_of_coins: int):
        """
        If the page is reloaded or the refresh button is pressed and enough time has elapsed, fetch new data. Update the data in the database.
        """
        crypto_info = GetCryptoData()
        data = crypto_info.get_quotes(number_of_coins)
        # Update database
        for coin in data:
            TopCrypto.objects.filter(name=coin['name']).update(price=coin['price'],market_cap=coin['market_cap'],percent_change_24h=coin['percent_change_24h'],percent_change_90d= coin['percent_change_90d'], symbol=coin['symbol'], rank=coin['rank'], time_stamp=timezone.now())

        return data

    def fetch_cached_data(self):
        return TopCrypto.objects.all()
