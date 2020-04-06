from django import forms
from . models import Preproject
# from preproject.models import Preproject, Customer

import django_filters

class Preprojectfilter(django_filters.FilterSet):
    customer__customer_name = django_filters.CharFilter(lookup_expr='icontains')
    project_name = django_filters.CharFilter(lookup_expr='icontains')
    pss_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')
    sales_lintasarta__name = django_filters.CharFilter(lookup_expr='icontains')
    sa_lintasarta__initial = django_filters.CharFilter(lookup_expr='icontains')
    # pss_ho_date = django_filters.BooleanFilter(field_name='pss_ho_date', lookup_expr='isnull', exclude=True)
    class Meta:
        model = Psa
        fields = [
                    'customer__customer_name',
                    'project_name',
                    'pss_lintasarta__name',
                    'sales_lintasarta__name',
                    'sa_lintasarta__initial'
                    # 'pss_ho_date',
                    # 'risk_category',
                    # 'status_psa'
                    ]