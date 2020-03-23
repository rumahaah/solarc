from django import forms
from . models import Psa, Pca
# from preproject.models import Preproject, Customer

import django_filters

class Psafilter(django_filters.FilterSet):
    preproject__oppty__customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__oppty__project_name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__pss_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__sales_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__sa_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Psa
        fields = [
                    'preproject__oppty__customer__customer_name',
                    'preproject__oppty__project_name','preproject__pss_lintasarta__name',
                    'preproject__sales_lintasarta__name',
                    'preproject__sa_lintasarta__name',
                    'risk_category'
                    ]

class Pcafilter(django_filters.FilterSet):
    psa__preproject__oppty__customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    psa__preproject__oppty__project_name = django_filters.CharFilter(lookup_expr='icontains')
    psa__preproject__sa_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Pca
        fields = [
                    'psa__preproject__oppty__customer__customer_name',
                    'psa__preproject__oppty__project_name',
                    'psa__preproject__sa_lintasarta__name',
                    'ebitda',
                    'irr'
                    ]