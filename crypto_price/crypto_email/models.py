from django.db import models
from django.utils import timezone


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
