from django import template
# from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import datetime
from psatopca.models import Psa, Pca, Preproject

register = template.Library()

@register.simple_tag
def psacount(preprojectid, *args, **kwargs):
	count = Psa.objects.filter(preproject__customer__id=preprojectid).count()
	return count

@register.simple_tag
def pcacount(preprojectid, *args, **kwargs):
	count = Pca.objects.filter(psa__preproject__customer__id=preprojectid).count()
	return count

@register.simple_tag
def woncount(preprojectid, *args, **kwargs):
	count = Preproject.objects.filter(customer__id=preprojectid).filter(progress='w').count()
	return count

@register.simple_tag
def lostcount(preprojectid, *args, **kwargs):
	count = Preproject.objects.filter(customer__id=preprojectid).filter(progress='l').count()
	return count