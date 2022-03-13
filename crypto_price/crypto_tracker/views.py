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
        
        #check if group exists, if not make a new group
        if TrackedCoinGroup.objects.all().filter(group_name=group).count() != 0:
            # group exits so just add it to the group
            group = TrackedCoinGroup.objects.get(group_name=group)
        else:
            # group doesn't exist so create a new group and add it to the group
            group = TrackedCoinGroup(group_name=group)
            group.save()

        new_tracked_crypto = group.trackedcoin_set.create(symbol=request.POST['symbol'], tracked_price = request.POST['tracked_price'], price = price, difference = difference)
        
        context = {'data': TrackedCoinGroup.objects.all()}
        print(context)
        
        return HttpResponseRedirect(reverse('crypto_tracker:tracker'), context)
    
    context = {'data': TrackedCoinGroup.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)


