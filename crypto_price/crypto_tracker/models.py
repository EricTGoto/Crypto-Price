from re import M
from django.db import models

class CryptoTracker(models.Model):
    symbol = models.CharField(max_length=5)
    tracked_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
