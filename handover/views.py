from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from . models import Handover
from . filters import Handoverfilter
from datetime import datetime
import numpy

# Create your views here.
# def ho_more_than_2wd_from_po_date(rawdata):
# 	my_list = []
# 	for handover in rawdata:
# 		check = numpy.busday_count(handover.po_date,datetime.now().date())
# 		if check >= 2:
# 			powas2wd = handover.id
# 			my_list.append(str(powas2wd))
# 	return my_list

def ho_more_than_2wd_from_po_known_date(rawdata):
	my_list = []
	for handover in rawdata:
		check = numpy.busday_count(handover.po_known_date,datetime.now().date())
		if check >= 2:
			my_list.append(str(handover.id))
	return my_list

@login_required
def handover (request,paramm='total'):
	if paramm == 'total':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.order_by(Lower('po_known_date').desc()))
	elif paramm == 'totalsa1':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.filter(pca__psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('po_known_date').desc()))
	elif paramm == 'totalsa2':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.filter(pca__psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('po_known_date').desc()))
	elif paramm == 'more2wdpoknowndate':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.filter(pk__in=ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(problem_category='n-pr'))).order_by(Lower('po_known_date').desc()))
	elif paramm == 'more2wdpoknowndatesa1':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.filter(pk__in=ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(problem_category='n-pr'))).filter(pca__psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('po_known_date').desc()))
	elif paramm == 'more2wdpoknowndatesa2':
		v_ho = Handoverfilter(request.GET, queryset=Handover.objects.filter(pk__in=ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(problem_category='n-pr'))).filter(pca__psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('po_known_date').desc()))
	else:
		v_ho = ''
	return render(request, 'handover.html',{
		'list': v_ho,
		})
