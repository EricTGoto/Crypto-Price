from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TrackedCoin, TrackedCoinGroup
from django.urls import reverse

from crypto_email.crypto_information import GetCryptoData

def tracker(request):
    crypto = GetCryptoData()
    if request.method == 'POST':
        context = TrackedCoinGroup.update_view(request)
        return HttpResponseRedirect(reverse('crypto_tracker:tracker'), context)

    context = {'data': TrackedCoinGroup.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)


