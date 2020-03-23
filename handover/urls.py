from django.urls import path

from . import views

urlpatterns = [
    path('ho', views.handover, name='handover'),
    path('ho/<slug:paramm>', views.handover),

]