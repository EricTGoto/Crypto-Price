from django.db import models

class TrackedCoinGroup(models.Model):
    group_name = models.CharField(max_length=10)

class TrackedCoin(models.Model):
    symbol = models.CharField(max_length=5)
    tracked_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trackedcoingroup = models.ForeignKey(TrackedCoinGroup, on_delete=models.CASCADE)


