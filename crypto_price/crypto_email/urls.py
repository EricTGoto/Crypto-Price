from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='crypto_email_index'),
]
