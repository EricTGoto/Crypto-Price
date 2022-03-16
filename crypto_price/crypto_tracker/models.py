from django.db import models
from crypto_email.crypto_information import GetCryptoData

class TrackedCoinGroup(models.Model):
    group_name = models.CharField(max_length=10)

    @classmethod
    def update_view(cls, request):
        group = request.POST['group']

        #check if group exists, if not make a new group
        if TrackedCoinGroup.objects.all().filter(group_name=group).count() != 0:
            # group exits so just add it to the group
            group = TrackedCoinGroup.objects.get(group_name=group)
        else:
            # group doesn't exist so create a new group and add it to the group
            group = TrackedCoinGroup(group_name=group)
            group.save()
        
        price_and_name = TrackedCoin.get_coin_price_and_name(request)
        difference = price_and_name[0] - int(request.POST['tracked_price'])

        new_tracked_crypto = group.trackedcoin_set.create(symbol=request.POST['symbol'], tracked_price = request.POST['tracked_price'], price = price_and_name[0], difference = difference, name=price_and_name[1])
        
        context = {'data': TrackedCoinGroup.objects.all()}

        return context

class TrackedCoin(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=5)
    tracked_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trackedcoingroup = models.ForeignKey(TrackedCoinGroup, on_delete=models.CASCADE)

    @classmethod
    def get_coin_price_and_name(cls, request):
        crypto = GetCryptoData()

        crypto_price = crypto.get_data_with_symbol(request.POST['symbol'])
        return (crypto_price['data'][f'{request.POST["symbol"]}']['quote']['USD']['price'], crypto_price['data'][f'{request.POST["symbol"]}']['name'])

class Coin(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=20)



    

