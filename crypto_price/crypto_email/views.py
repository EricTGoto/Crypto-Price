from django.shortcuts import render
from django.http import HttpResponse
from . import crypto_information
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
    crypto_info = crypto_information.GetCryptoData()
    map_data = crypto_info.get_top_coins(5)
    data = crypto_info.clean_map_response(map_data)
    ids = crypto_info.get_IDs(map_data)
    quotes= crypto_info.get_data(ids)
    data = crypto_info.add_coin_data_from_quotes_latest(quotes, data)
    print(data)
    
    context = { 'data': data }
    return render(request, 'crypto_email/index.html', context)

def about(request):
    return render(request, 'crypto_email/about.html', {'title': 'About'})