from django import forms
from . models import Preproject
# from preproject.models import Preproject, Customer

import django_filters

class Preprojectfilter(django_filters.FilterSet):
    customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    project_name = django_filters.CharFilter(lookup_expr='icontains')
    pss_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    sales_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    sa_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    # pss_ho_date = django_filters.BooleanFilter(field_name='pss_ho_date', lookup_expr='isnull', exclude=True)
    class Meta:
        model = Preproject
        fields = [
                    'customer__customer_name',
                    'project_name',
                    'pss_lintasarta__initial',
                    'sales_lintasarta__initial',
                    'sa_lintasarta__initial',
                    'sa_lintasarta__subbag',
                    'project_status',
                    'solution_criteria',
                    'progress',
                    'taxsonomi',
                    'payment'
                    ]