from django.urls import path

from . import views

urlpatterns = [
    path('oppty', views.preproject, name='preproject'),
    path('oppty/<slug:paramm>', views.preproject),
    path('customer', views.customer_list, name='customer_list'),
]