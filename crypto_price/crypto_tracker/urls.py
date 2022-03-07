from django.urls import path
from . import views

app_name = 'crypto_tracker'

urlpatterns = [
    path('', views.tracker, name='tracker'),
]
