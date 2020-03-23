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
		# check_again = numpy.busday_count(handover.po_known_date,handover.submit_presales_handover_date)
		# if check_again <=2 and check >= 2:
		# 	my_list.remove(str(handover.id))
	return my_list


def handover (request,paramm='total'):
	data = Handover.objects.order_by(Lower('po_known_date').desc())
	# data = Handover.objects.exclude(problem_category='n-pr').order_by(Lower('po_known_date').desc())
	if paramm == 'total':
		# v_ho = Handover.objects.order_by(Lower('psa_date').desc())
		# v_ho = data
		v_ho = Handoverfilter(request.GET, queryset=data)
	# elif paramm == 'more2wdpodate':
	# 	a = ho_more_than_2wd_from_po_date(data)
	# 	v_ho = Handover.objects.filter(pk__in=a).order_by(Lower('po_known_date').desc())
	elif paramm == 'more2wdpoknowndate':
		a = ho_more_than_2wd_from_po_known_date(data)
		v_ho = Handover.objects.filter(pk__in=a).exclude(problem_category='n-pr').order_by(Lower('po_known_date').desc())

	# 	v_psa = Psa.objects.filter(status_psa='g').order_by(Lower('psa_date').desc())
	# elif paramm == 'not':
	# 	v_psa = Psa.objects.exclude(status_psa='g').order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wd':
	# 	# a = Psa.objects.all()
	# 	a = Psa.objects.filter(status_psa='g')
	# 	b = psa_more_than_5wd(a)
	# 	v_psa = Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho':
	# 	# a = Psa.objects.all()
	# 	a = Psa.objects.filter(status_psa='g')
	# 	b = psa_more_than_5wd_from_pss_ho(a)
	# 	v_psa = Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc())
	else:
		v_ho = ''
	return render(request, 'handover.html',{
		'list': v_ho,
		})
