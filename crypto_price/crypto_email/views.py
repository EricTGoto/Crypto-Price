from django.shortcuts import render
from django.http import HttpResponse
from . import crypto_information
# Create your views here.

data = [
    {
        'name': "Ethereum",
        'price': "10000"
    }
]

def index(request):
    #crypto_info = crypto_information.GetCryptoData()
    #raw_data = crypto_info.getData()
    #data = crypto_info.extractInfo(raw_data, '1027')
    #print(data)
    context = { 'data': data }
    return render(request, 'crypto_email/index.html', context)

def about(request):
    return render(request, 'crypto_email/about.html', {'title': 'About'})