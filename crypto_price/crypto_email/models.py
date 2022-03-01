from django.db import models
from django.utils import timezone
from .crypto_information import GetCryptoData

class Top5Crypto(models.Model):
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

    def fetch_data(self):
        # If database is empty, then fetch data from CoinMarketCap.
        if Top5Crypto.objects.all().count() == 0:
            print("initial fetch data")
            return self.initial_data_fetch()
        # If database is not empty and the cached data is more than x minutes old then fetch new data.
        elif (timezone.now() - Top5Crypto.objects.first().time_stamp).seconds/60 >= 0.2:
            print("fetch new data")
            return self.fetch_new_data()
        # If database is not empty and cached data is less than x minutes old, grab the cached data
        else:
            print("cached data")
            return Top5Crypto.objects.all()

    def initial_data_fetch(self):
        """
        When the website is accessed for the first time, the database will be empty so data will have to be fetched with the CMC API and then cached in to the database.
        """
        crypto_info = GetCryptoData()
        map_data = crypto_info.get_top_coins(5)
        data = crypto_info.clean_map_response(map_data)
        ids = crypto_info.get_IDs(map_data)
        quotes= crypto_info.get_data_from_cmp(ids)
        data = crypto_info.add_coin_data_from_quotes_latest(quotes, data)

        # Cache into database
        for coin in data:
            new_data = Top5Crypto(name=coin['name'],price=coin['price'],market_cap=coin['market_cap'],percent_change_24h=coin['percent_change_24h'],percent_change_90d= coin['percent_change_90d'], symbol=coin['symbol'], rank=coin['rank'])
            new_data.save()

        return data

    def fetch_new_data(self):
        """
        If the page is reloaded or the refresh button is pressed and enough time has elapsed, fetch new data. Update the data in the database.
        """
        crypto_info = GetCryptoData()
        map_data = crypto_info.get_top_coins(5)
        data = crypto_info.clean_map_response(map_data)
        ids = crypto_info.get_IDs(map_data)
        quotes= crypto_info.get_data_from_cmp(ids)
        data = crypto_info.add_coin_data_from_quotes_latest(quotes, data)

        for coin in data:
            Top5Crypto.objects.filter(name=coin['name']).update(price=coin['price'],market_cap=coin['market_cap'],percent_change_24h=coin['percent_change_24h'],percent_change_90d= coin['percent_change_90d'], symbol=coin['symbol'], rank=coin['rank'], time_stamp=timezone.now())

        return data

    def fetch_cached_data(self):
        return Top5Crypto.objects.all()
