from django.shortcuts import render
from django.http import HttpResponse
from . import crypto_information
from .models import Top5Crypto
from django.utils import timezone

def index(request):
    data = Top5Crypto.fetch_data()
    context = { 'data': data }
    return render(request, 'crypto_email/index.html', context)

def about(request):
    return render(request, 'crypto_email/about.html', {'title': 'About'})