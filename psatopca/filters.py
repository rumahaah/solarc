from django import forms
from . models import Psa, Pca
# from preproject.models import Preproject, Customer

import django_filters

class Psafilter(django_filters.FilterSet):
    preproject__customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__project_name = django_filters.CharFilter(lookup_expr='icontains')
    preproject__pss_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    preproject__sales_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    preproject__sa_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    pss_ho_date = django_filters.BooleanFilter(field_name='pss_ho_date', lookup_expr='isnull', exclude=True)
    class Meta:
        model = Psa
        fields = [
                    'preproject__customer__customer_name',
                    'preproject__project_name','preproject__pss_lintasarta__initial',
                    'preproject__sales_lintasarta__initial',
                    'preproject__sa_lintasarta__initial',
                    'preproject__progress',
                    'risk_category',
                    'psa_date',
                    'pss_ho_date',
                    'status_psa'
                    ]

class Pcafilter(django_filters.FilterSet):
    psa__preproject__customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    psa__preproject__project_name = django_filters.CharFilter(lookup_expr='icontains')
    psa__preproject__sa_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    psa__pss_ho_date = django_filters.BooleanFilter(field_name='psa__pss_ho_date', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Pca
        fields = [
                    'psa__preproject__customer__customer_name',
                    'psa__preproject__project_name',
                    'psa__preproject__sa_lintasarta__initial',
                    'psa__preproject__progress',
                    'psa__pss_ho_date',
                    'psa__status_psa',
                    'ebitda',
                    'irr',
                    'status_pca'
                    ]