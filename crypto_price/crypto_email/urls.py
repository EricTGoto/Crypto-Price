from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='crypto_email_index'),
    path('about/', views.about, name='crpyto_email_about'),
]
