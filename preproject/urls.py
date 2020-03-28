from django.urls import path

from . import views

urlpatterns = [
    path('oppty', views.preproject, name='preproject'),
    path('oppty/<slug:paramm>', views.preproject),
    path('detailpersa', views.detailpersa, name='detailpersa'),
    path('detailpersa/<slug:paramm>', views.detailpersa),
    path('opptywon', views.opptywon, name='opptywon'),
    path('opptylost', views.opptylost, name='opptylost'),
    path('customer', views.customer_list, name='customer_list'),
]