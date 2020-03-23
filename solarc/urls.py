"""solarc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from dashboard import views as dashboard_view
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views



admin.site.site_header = "SolArc Admin"
admin.site.site_title = "SolArc site admin"

urlpatterns = [
    path('', dashboard_view.home , name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('psapca/', include('psatopca.urls')),
    path('preproject/', include('preproject.urls')),
    path('handover/', include('handover.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/login/', login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', dashboard_view.about , name='about'),
    # path('accounts/', include('django.contrib.auth.urls')),
]
