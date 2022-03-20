from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TrackedCoin, TrackedCoinGroup
from django.urls import reverse

def tracker(request):
    # if request is a post, update the page
    if request.method == 'POST':   
        context = TrackedCoinGroup.update_view(request)
        return HttpResponseRedirect(reverse('crypto_tracker:tracker'), context)
    # if request is a get, just display data from DB
    context = {'data': TrackedCoinGroup.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)

def delete_item(request):
    group_name = ""
    for key in request.POST.dict().keys():
        if key != 'csrfmiddlewaretoken': group_name = key
    
    TrackedCoinGroup.objects.get(group_name=group_name).delete()
    context = {'data': TrackedCoinGroup.objects.all()}
    return render(request, 'crypto_tracker/tracker.html', context)