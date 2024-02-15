from django.urls import path
from .views import PriceCalculatorAPI

urlpatterns = [
    path('calculate-price/', PriceCalculatorAPI.as_view(), name='calculate_price'),
]
