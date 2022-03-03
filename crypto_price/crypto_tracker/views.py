from django.shortcuts import render

def tracker(request):
    return render(request, 'crypto_tracker/tracker.html')