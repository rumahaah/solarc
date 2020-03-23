from django import forms
from . models import Handover
# from preproject.models import Preproject, Customer

import django_filters

class Handoverfilter(django_filters.FilterSet):
    pca__psa__preproject__oppty__customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    pca__psa__preproject__oppty__project_name = django_filters.CharFilter(lookup_expr='icontains')
    pca__psa__preproject__sa_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Handover
        fields = [
                    'pca__psa__preproject__oppty__customer__customer_name',
                    'pca__psa__preproject__oppty__project_name',
                    'pca__psa__preproject__sa_lintasarta__name',
                    'problem_category',
                    ]