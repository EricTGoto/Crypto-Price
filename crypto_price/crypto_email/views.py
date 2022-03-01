from django.shortcuts import render
from django.http import HttpResponse
from . import crypto_information
from .models import Top5Crypto
from django.utils import timezone
# Create your views here.

data = [
    {
        'name': "Ethereum",
        'price': "10000"
    },
    {
        'name': "Bitcoin",
        'price': "10000"
    },
    {
        'name': "Dogecoin",
        'price': "5"
    },
    {
        'name': "Scamcoin",
        'price': "21123"
    },
    {
        'name': "Ponzicoin",
        'price': "511"
    }
]

def index(request):
    data = Top5Crypto.fetch_data()
    context = { 'data': data }
    return render(request, 'crypto_email/index.html', context)

def about(request):
    return render(request, 'crypto_email/about.html', {'title': 'About'})