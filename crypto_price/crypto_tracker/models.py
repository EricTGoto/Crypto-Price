from django.db import models
from crypto_email.crypto_information import GetCryptoData

class Coin(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=20)

class TrackedCoinGroup(models.Model):
    group_name = models.CharField(max_length=10)

    @classmethod
    def update_view(cls, request):
        crypto_data = GetCryptoData()
        group = request.POST['group']
        symbol = request.POST['symbol']

        #check if group exists, if not make a new group
        if TrackedCoinGroup.objects.all().filter(group_name=group).count() != 0:
            # group exits so just add it to the group
            group = TrackedCoinGroup.objects.get(group_name=group)
        else:
            # group doesn't exist so create a new group
            group = TrackedCoinGroup(group_name=group)
            group.save()

        coin_info = crypto_data.get_data_with_symbol(symbol)
        #check if coin exists
        # if coin doesn't exist, create and return new info
        # TODO: return new info
        if Coin.objects.filter(name=coin_info['name']).count() == 0:
            coin_info = crypto_data.get_data_with_symbol(symbol)
            coin = Coin(symbol=coin_info['symbol'], name=coin_info['name'])
            coin.save()
        else:
            # coin exists, so we create a new trackedcoin under the appropriate coin and trackedcoingroup
            # TODO: return already existing info
            coin = Coin.objects.get(name=coin_info['name'])
            
        difference = coin_info['price'] - int(request.POST['tracked_price'])    
        coin.trackedcoin_set.create(symbol=request.POST['symbol'], tracked_price = request.POST['tracked_price'], price = coin_info['price'], difference = difference, name=coin_info['name'], trackedcoingroup = group)
        context = {'data': TrackedCoinGroup.objects.all()}

        return context

class TrackedCoin(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=5)
    tracked_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trackedcoingroup = models.ForeignKey(TrackedCoinGroup, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)





    

