from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TrackedCoin, TrackedCoinGroup
from django.urls import reverse

from crypto_email.crypto_information import GetCryptoData

def tracker(request):
    crypto = GetCryptoData()
    if request.method == 'POST':

        print("POST")
        print(request.POST)
        crypto_price = crypto.get_data_with_symbol(request.POST['symbol'])
        price = crypto_price['data'][f'{request.POST["symbol"]}']['quote']['USD']['price']

        # difference is positive if current price is greater than tracked price
        difference = price - int(request.POST['tracked_price'])
        group = request.POST['group']
        
        new_group = TrackedCoinGroup(group_name=group)
        new_group.save()
        new_tracked_crypto = new_group.trackedcoin_set.create(symbol=request.POST['symbol'], tracked_price = request.POST['tracked_price'], price = price, difference = difference)
        
        # extract the coin groups from the tracked
        context = {'data': TrackedCoinGroup.objects.all()}
        print(context)
        
        return HttpResponseRedirect(reverse('crypto_tracker:tracker'), context)
    
    context = {'data': TrackedCoin.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)


