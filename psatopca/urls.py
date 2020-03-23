from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='psapca_home'),
    path('psa', views.index_psa, name='psa'),
    path('psa/<slug:paramm>', views.index_psa),
    path('pca', views.index_pca, name='pca'),
    path('pca/<slug:paramm>', views.index_pca),
    # path('psa5wd', views.psa5wd, name='psa5wd'),
    # path('psa5wdpssho', views.psa5wdpssho, name='psa5wdpssho'),

]