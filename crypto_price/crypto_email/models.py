from django.db import models
from django.utils import timezone
from .crypto_information import GetCryptoData

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
            print("initial fetch data")
            return self.initial_data_fetch(number_of_coins)
        # If database is not empty and the cached data is more than x minutes old then fetch new data.
        elif (timezone.now() - TopCrypto.objects.first().time_stamp).seconds/60 >= 15:
            print("fetch new data")
            return self.fetch_new_data(number_of_coins)
        # If database is not empty and cached data is less than x minutes old, grab the cached data
        else:
            print("cached data")
            return TopCrypto.objects.all()

    def initial_data_fetch(self, number_of_coins: int):
        """
        When the website is accessed for the first time, the database will be empty so data will have to be fetched with the CMC API and then cached in to the database.
        """
        crypto_info = GetCryptoData()
        data = crypto_info.get_quotes(number_of_coins)

        # Cache into database
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

        for coin in data:
            TopCrypto.objects.filter(name=coin['name']).update(price=coin['price'],market_cap=coin['market_cap'],percent_change_24h=coin['percent_change_24h'],percent_change_90d= coin['percent_change_90d'], symbol=coin['symbol'], rank=coin['rank'], time_stamp=timezone.now())

        return data

    def fetch_cached_data(self):
        return TopCrypto.objects.all()
