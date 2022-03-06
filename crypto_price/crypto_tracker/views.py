from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import CryptoTracker

def tracker(request):

    if request.method == 'POST':
        print("POST")
        print(request.POST)
        new_tracked_crypto = CryptoTracker(symbol=request.POST['symbol'], tracked_price = request.POST['price'])
        new_tracked_crypto.save()

    context = {'data': CryptoTracker.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)


