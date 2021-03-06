from django.urls import path

from . import views

urlpatterns = [
    path('oppty', views.preproject, name='preproject'),
    path('oppty/<slug:paramm>', views.preproject),
    path('detail', views.detail, name='detail'),
    path('detail/<slug:paramm>', views.detail),
    path('opptywon', views.opptywon, name='opptywon'),
    path('opptylost', views.opptylost, name='opptylost'),
    path('customer', views.customer_list, name='customer_list'),
    path('customer/<slug:paramm>', views.customer_list),
    path('customerdetail/<slug:paramm>', views.customer_list_detail),
    path('opptyraw', views.opptyraw, name='opptyraw'),
]