from django.urls import path

from . import views

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('subbag', views.Dashboardsubbag, name='dashboard_subbag'),
    path('subbag/<slug:paramm>', views.Dashboardsubbag),
]