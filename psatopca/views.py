from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.db.models import Avg

from . models import Psa, Pca
from . filters import Psafilter, Pcafilter

from datetime import datetime
import numpy
import statistics 

# Create your views here.
# register = template.Library()

# @register.simple_tag
# def totalcontracvalue(mrc, otc, duration, *args, **kwargs):
#     # you would need to do any localization of the result here
#     return ( mrc * duration ) + otc

#help_function
def psa_more_than_5wd (rawdata):
	my_list = []
	remove_list_b = []
	for psa in rawdata:
		pcas = psa.pca_set.all()
		calculation = numpy.busday_count(psa.psa_date,datetime.now().date())
		if calculation >= 5:
			my_list.append(psa.id)
		for pca in pcas:
			check = numpy.busday_count(psa.psa_date,pca.pca_date)
			if calculation >= 5 and check <= 5:
				remove_list_b.append(pca.psa_id)
			a = set(remove_list_b)
			remove_list_e = list(a)
	for apa in remove_list_e:
		my_list.remove(apa)

	return my_list

def psa_more_than_5wd_from_pss_ho (rawdata):
	my_list = []
	remove_list_b = []
	for psa in rawdata:
		# psa_date = psa.psa_date
		pcas = psa.pca_set.all()
		calculation = numpy.busday_count(psa.psa_date,datetime.now().date())
		if calculation >= 5:
			my_list.append(psa.id)
		for pca in pcas:
			check = numpy.busday_count(psa.pss_ho_date,pca.pca_date)
			if calculation >=5 and check <= 5:
				remove_list_b.append(pca.psa_id)
			a = set(remove_list_b)
			remove_list_e = list(a)
	for apa in remove_list_e:
		my_list.remove(apa)

	return my_list

def progressafterpca_21days (rawdata):
	my_list = []
	for pca in rawdata:
		calculation = datetime.now().date() - pca.pca_date
		if calculation.days >=21:
		# if calculation.days >=3:
			# pcamorethan30wd = pca.id
			# my_list.append(str(pcamorethan30wd))
			progress = pca.psa.preproject.progress
			if progress == 'p':
				stillproress = pca.id
				my_list.append(str(stillproress))
			if progress == 's':
				stillproress = pca.id
				my_list.append(str(stillproress))
	return my_list

#viewtotemplate
@login_required
def index_psa (request,paramm='total'):
	if paramm == 'total':
		aa = Psa.objects.order_by(Lower('psa_date').desc())
		v_psa = Psafilter(request.GET, queryset=aa)
	elif paramm == 'go':
		# v_psa = Psa.objects.filter(status_psa='g').order_by(Lower('psa_date').desc())
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(status_psa='g').order_by(Lower('psa_date').desc()))
	# elif paramm == 'go-satbc':
		# v_psa = Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta=7).order_by(Lower('psa_date').desc())
		# v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta=7).order_by(Lower('psa_date').desc()))
	elif paramm == 'not':
		# v_psa = Psa.objects.exclude(status_psa='g').order_by(Lower('psa_date').desc())
		v_psa = Psafilter(request.GET, queryset=Psa.objects.exclude(status_psa='g').order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wd':
		# a = Psa.objects.all()
		# a = Psa.objects.filter(status_psa='g')
		a = Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')
		b = psa_more_than_5wd(a)
		# v_psa = Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc())
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpssho':
		# a = Psa.objects.all()
		a = Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')
		b = psa_more_than_5wd_from_pss_ho(a)
		# aa = Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc())
		# aa = Psa.objects.order_by(Lower('psa_date').desc())
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=b).order_by(Lower('psa_date').desc()))
	# elif paramm == 'psa5wdpssho-ggw':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=1))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-irs':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=2))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-mgm':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=3))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-sdr':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=4))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-tmb':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=5))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-zkf':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=6))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-wit':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=8))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-dpm':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=9))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-mbo':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=10))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-aju':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=11))).order_by(Lower('psa_date').desc())
	# elif paramm == 'psa5wdpssho-muh':
	# 	v_psa = Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta=12))).order_by(Lower('psa_date').desc())
	elif paramm == 'psa5wdpssho-sa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(sub_dept='sa1').filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpssho-sa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(sub_dept='sa2').filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	else:
		v_psa = ''
	return render(request, 'psa.html',{
	# return render(request, 'psa_oioi.html',{
		'list': v_psa,
		})


# @login_required
# def psa5wd (request):
# 	v_psa = Psa.objects.all()
# 	v_list_id_psa_more_than_5wd = psa_more_than_5wd(v_psa)
# 	v_psalist_more_than_5wd = Psa.objects.filter(pk__in=v_list_id_psa_more_than_5wd)

# 	return render(request, 'psa.html',{
# 		'list': v_psalist_more_than_5wd,
# 		})

# @login_required
# def psa5wdpssho (request):
# 	v_psa = Psa.objects.all()
# 	v_list_id_psa_more_than_5wd = psa_more_than_5wd_from_pss_ho(v_psa)
# 	v_psalist_more_than_5wd = Psa.objects.filter(pk__in=v_list_id_psa_more_than_5wd)

# 	return render(request, 'psa.html',{
# 		'list': v_psalist_more_than_5wd,
# 		})

@login_required
def index_pca (request,paramm='total'):
	if paramm == 'total':
		# v_pca = Pca.objects.order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.order_by(Lower('pca_date').desc()))
	elif paramm == 'go':
		# v_pca = Pca.objects.filter(status_pca='g').order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(status_pca='g').order_by(Lower('pca_date').desc()))
	elif paramm == 'not':
		# v_pca = Pca.objects.exclude(status_pca='g').order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(status_pca='g').order_by(Lower('pca_date').desc()))
	elif paramm == 'pca21wd':
		a = Pca.objects.filter(status_pca='g')
		b = progressafterpca_21days(a)
		# v_pca = Pca.objects.filter(pk__in=b).order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=b).order_by(Lower('pca_date').desc()))
	elif paramm == 'pcaebitda':
		# v_pca = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').order_by(Lower('pca_date').desc()))
	elif paramm == 'pcairr':
		# v_pca = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').order_by(Lower('pca_date').desc())
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').order_by(Lower('pca_date').desc()))
	elif paramm == 'pcaksaea':
		my_list = []
		for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
			my_list.append(str(pca.id))
		for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
			my_list.append(str(pca.id))
		my_list_winlost = []
		for pca in Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='w'):
			my_list_winlost.append(str(pca.id))
		for pca in Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='l'):
			my_list_winlost.append(str(pca.id))
		# v_pca = Pca.objects.filter(pk__in=my_list_winlost)
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=my_list_winlost))
	elif paramm == 'pcanonksaea':
		my_list = []
		for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
			my_list.append(str(pca.id))
		for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
			my_list.append(str(pca.id))
		my_list_winlost = []
		for pca in Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='w'):
			my_list_winlost.append(str(pca.id))
		for pca in Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='l'):
			my_list_winlost.append(str(pca.id))
		# v_pca = Pca.objects.filter(pk__in=my_list_winlost)
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=my_list_winlost))
	else:
		v_psa = ''

	return render(request, 'pca.html',{
	# return render(request, 'pcawin.html',{
		'list': v_pca,
		})

def ebitdaprofitability():
	avgebitda = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').aggregate(Avg('ebitda'))
	datas = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').values_list('duration','otc','mrc','ebitda')
	sum_tcv = sum(data[0] * data[2] + data[1] for data in datas)
	sum_ebitda_weighted = 0
	for data in datas:
		weighted = ((data[0] * data[2]) + data[1]) / sum_tcv
		ebitda_weighted = data[3] * weighted
		sum_ebitda_weighted += ebitda_weighted
	return [round(avgebitda['ebitda__avg'],1), round(sum_ebitda_weighted,1)]

def irrprofitability():
	avgirr = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').aggregate(Avg('irr'))
	datas = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').values_list('duration','otc','mrc','irr')
	sum_tcv = sum(data[0] * data[2] + data[1] for data in datas)
	sum_irr_weighted = 0
	for data in datas:
		weighted = ((data[0] * data[2]) + data[1]) / sum_tcv
		irr_weighted = data[3] * weighted
		sum_irr_weighted += irr_weighted
	return [round(avgirr['irr__avg'],1), round(sum_irr_weighted,1)]

def winrate_ksaea():
	my_list = []
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
		my_list.append(str(pca.id))
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
		my_list.append(str(pca.id))
	list_ksaea_won = Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='w').values_list('duration','otc','mrc')
	list_ksaea_lost = Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='l').values_list('duration','otc','mrc')
	sum_tcv_won = sum(data[0] * data[2] + data[1] for data in list_ksaea_won)
	sum_tcv_lost = sum(data[0] * data[2] + data[1] for data in list_ksaea_lost)
	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
	return [round(winrate,1), sum_tcv_won, sum_tcv_lost]

def winrate_nonksaea():
	my_list = []
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
		my_list.append(str(pca.id))
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
		my_list.append(str(pca.id))
	list_ksaea_won = Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='w').values_list('duration','otc','mrc')
	list_ksaea_lost = Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='l').values_list('duration','otc','mrc')
	sum_tcv_won = sum(data[0] * data[2] + data[1] for data in list_ksaea_won)
	sum_tcv_lost = sum(data[0] * data[2] + data[1] for data in list_ksaea_lost)
	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
	return [round(winrate,1), sum_tcv_won, sum_tcv_lost]

def risk_criteria():
	hr = Psa.objects.filter(risk_category='h')
	mr = Psa.objects.filter(risk_category='m')
	lr = Psa.objects.filter(risk_category='l')
	return [hr,mr,lr]

