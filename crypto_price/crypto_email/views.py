from django.shortcuts import render
from django.http import HttpResponse
from .models import TopCrypto

def index(request):
    crypto_api = TopCrypto()
    data= crypto_api.fetch_data(10)
    context = { 'data': data }
    return render(request, 'crypto_email/index.html', context)

def about(request):
    return render(request, 'crypto_email/about.html', {'title': 'About'})