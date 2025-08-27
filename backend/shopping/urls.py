from .views import *
from django.urls import path

urlpatterns = [
    path('scrap_supermarket', SupermarketScrapingView.as_view(), name='scrap_supermarket'),
]