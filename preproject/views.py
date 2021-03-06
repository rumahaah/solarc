from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.db.models import Count

from . models import Preproject, Customer
from psatopca.models import Psa, Pca
from . filters import Preprojectfilter

# Create your views here.
# def preproprogres ():
# 	my_list = []
# 	for preproject in Preproject.objects.filter(progress='s'):
# 		identity = preproject.id
# 		my_list.append(str(identity))
# 	for preproject in Preproject.objects.filter(progress='p'):
# 		identity = preproject.id
# 		my_list.append(str(identity))
# 	return my_list

# def exclude_preproprogres ():
# 	my_list = []
# 	for preproject in Preproject.objects.all():
# 		my_list.append(preproject.id)
# 	for preproject in Preproject.objects.filter(progress='s'):
# 		my_list.remove(preproject.id)
# 	for preproject in Preproject.objects.filter(progress='p'):
# 		my_list.remove(preproject.id)
# 	return my_list

def oppty_per_customer():
	ksa = Preproject.objects.filter(customer__customer_criteria='0').count()
	ea = Preproject.objects.filter(customer__customer_criteria='1').count()
	sa = Preproject.objects.filter(customer__customer_criteria='2').count()
	x = Preproject.objects.filter(customer__customer_criteria='3').count()
	y = Preproject.objects.filter(customer__customer_criteria='4').count()
	others = x + y
	return [ksa,ea,sa,others]

@login_required
def preproject (request,paramm='all'):
	if paramm == 'all':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.all())
	elif paramm == 'allsa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(sa_lintasarta__subbag='1'))
	elif paramm == 'allsa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(sa_lintasarta__subbag='2'))
	elif paramm == 'progresssa':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='p'))
	elif paramm == 'progresssa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='p').filter(sa_lintasarta__subbag='1'))
	elif paramm == 'progresssa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='p').filter(sa_lintasarta__subbag='2'))
	elif paramm == 'submited':
		v_preproject =  Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='s'))
	elif paramm == 'submitedsa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='s').filter(sa_lintasarta__subbag='1'))
	elif paramm == 'submitedsa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='s').filter(sa_lintasarta__subbag='2'))
	elif paramm == 'closewon':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='w'))
	elif paramm == 'closewonsa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='w').filter(sa_lintasarta__subbag='1'))
	elif paramm == 'closewonsa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='w').filter(sa_lintasarta__subbag='2'))
	elif paramm == 'closelost':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='l'))
	elif paramm == 'closelostsa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='l').filter(sa_lintasarta__subbag='1'))
	elif paramm == 'closelostsa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='l').filter(sa_lintasarta__subbag='2'))
	elif paramm == 'cancelled_psahold':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(progress='c') | Preproject.objects.filter(progress='h'))
	elif paramm == 'cancelled_psaholdsa1':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='c') | Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='h'))
	elif paramm == 'cancelled_psaholdsa2':
		v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='c') | Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='h'))
	else:
		v_preproject =''

	return render(request, 'preproject.html',{
		'list': v_preproject,
	})

@login_required
def opptyraw (request):
	# v_preproject = Preproject.objects.all().filter(id=115)
	v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.all())
	# v_preproject = Preprojectfilter(request.GET, queryset=Preproject.objects.all().filter(id=42))
	return render(request, 'preproject_opptyraw.html',{
		'list': v_preproject,
	})

@login_required
def opptywon (request):
	v_preproject = Preproject.objects.filter(progress='w')
	return render(request, 'preproject_wonlost.html',{
		'list': v_preproject,
	})

@login_required
def opptylost (request):
	v_preproject = Preproject.objects.filter(progress='l')
	return render(request, 'preproject_wonlost.html',{
		'list': v_preproject,
	})

@login_required
def detail (request,paramm='n'):
	if paramm == 'n':
		v_list = ''
		v_total_psa = ''
		v_total_pca = ''
		v_total_psa_l = ''
		v_total_psa_m = ''
		v_total_psa_s = ''
		v_total_psa_hr = ''
		v_total_psa_mr = ''
		v_total_psa_lr = ''
		tittle = ''
		v_total_won = ''
		v_total_lost = ''
		v_total_progress = ''
		v_total_cancelled = ''
	elif paramm == 'sa1':
		v_list = Preproject.objects.filter(sa_lintasarta__subbag='1').order_by('sa_lintasarta__initial')
		v_total_psa = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').count()
		v_total_pca = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').count()
		v_total_psa_l = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(scale='l').count()
		v_total_psa_m = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(scale='m').count()
		v_total_psa_s = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(scale='s').count()
		v_total_psa_hr = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(risk_category='h').count()
		v_total_psa_mr = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(risk_category='m').count()
		v_total_psa_lr = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(risk_category='l').count()
		tittle = 'SA 1'
		v_total_won = Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='w').count()
		v_total_lost = Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='l').count()
		v_total_progress = Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='p').count() + Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='s').count()
		v_total_cancelled = Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='c').count() + Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='h').count()
	elif paramm == 'sa2':
		v_list = Preproject.objects.filter(sa_lintasarta__subbag='2').order_by('sa_lintasarta__initial')
		v_total_psa = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').count()
		v_total_pca = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').count()
		v_total_psa_l = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(scale='l').count()
		v_total_psa_m = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(scale='m').count()
		v_total_psa_s = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(scale='s').count()
		v_total_psa_hr = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(risk_category='h').count()
		v_total_psa_mr = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(risk_category='m').count()
		v_total_psa_lr = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(risk_category='l').count()
		tittle = 'SA 2'
		v_total_won = Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='w').count()
		v_total_lost = Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='l').count()
		v_total_progress = Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='p').count() + Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='s').count()
		v_total_cancelled = Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='c').count() + Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='h').count()
	elif paramm == 'all':
		v_list = Preproject.objects.order_by('sa_lintasarta__initial')
		v_total_psa = Psa.objects.count()
		v_total_pca = Pca.objects.count()
		v_total_psa_l = Psa.objects.filter(scale='l').count()
		v_total_psa_m = Psa.objects.filter(scale='m').count()
		v_total_psa_s = Psa.objects.filter(scale='s').count()
		v_total_psa_hr = Psa.objects.filter(risk_category='h').count()
		v_total_psa_mr = Psa.objects.filter(risk_category='m').count()
		v_total_psa_lr = Psa.objects.filter(risk_category='l').count()
		tittle = 'ALL'
		v_total_won = Preproject.objects.filter(progress='w').count()
		v_total_lost = Preproject.objects.filter(progress='l').count()
		v_total_progress = Preproject.objects.filter(progress='p').count() + Preproject.objects.filter(progress='s').count()
		v_total_cancelled = Preproject.objects.filter(progress='c').count() + Preproject.objects.filter(progress='h').count()
	else:
		v_list = Preproject.objects.filter(sa_lintasarta__initial=paramm)
		v_total_psa = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).count()
		v_total_pca = Pca.objects.filter(psa__preproject__sa_lintasarta__initial=paramm).count()
		v_total_psa_l = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(scale='l').count()
		v_total_psa_m = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(scale='m').count()
		v_total_psa_s = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(scale='s').count()
		v_total_psa_hr = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(risk_category='h').count()
		v_total_psa_mr = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(risk_category='m').count()
		v_total_psa_lr = Psa.objects.filter(preproject__sa_lintasarta__initial=paramm).filter(risk_category='l').count()
		tittle = paramm
		v_total_won = Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='w').count()
		v_total_lost = Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='l').count()
		v_total_progress = Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='p').count() + Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='s').count()
		v_total_cancelled = Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='c').count() + Preproject.objects.filter(sa_lintasarta__initial=paramm).filter(progress='h').count()

	# return render(request, 'preproject_detailpersa.html',{
	return render(request, 'preproject_detailpersa_accordion.html',{
		'list': v_list,
		'totalpsa': v_total_psa,
		'totalpca': v_total_pca,
		'totalpsa_l': v_total_psa_l,
		'totalpsa_m': v_total_psa_m,
		'totalpsa_s': v_total_psa_s,
		'totalpsa_hr': v_total_psa_hr,
		'totalpsa_mr': v_total_psa_mr,
		'totalpsa_lr': v_total_psa_lr,
		'tittle': tittle,
		'totalwon': v_total_won,
		'totalprogress': v_total_progress,
		'totalcancelled': v_total_cancelled,
	})


@login_required
def customer_list(request,paramm='all'):
	if paramm == 'all':
		v_customer = Customer.objects.all().annotate(num_oppty=Count('preproject')).order_by(Lower('customer_criteria'))
	elif paramm == 'ska':
		v_customer = Customer.objects.filter(customer_criteria='0').annotate(num_oppty=Count('preproject')).order_by(Lower('customer_segment'))
	elif paramm == 'ea':
		v_customer = Customer.objects.filter(customer_criteria='1').annotate(num_oppty=Count('preproject'))
	elif paramm == 'ka':
		v_customer = Customer.objects.filter(customer_criteria='2').annotate(num_oppty=Count('preproject'))
	elif paramm == 'ra':
		v_customer = Customer.objects.filter(customer_criteria='3').annotate(num_oppty=Count('preproject')) | Customer.objects.filter(customer_criteria='4').annotate(num_oppty=Count('preproject'))
	elif paramm == 'skaea':
		v_customer = Customer.objects.filter(customer_criteria='0').annotate(num_oppty=Count('preproject')).order_by(Lower('customer_criteria')) | Customer.objects.filter(customer_criteria='1').annotate(num_oppty=Count('preproject')).order_by(Lower('customer_criteria'))

	return render(request, 'customer.html',{
	'list': v_customer,
	})

@login_required
def customer_list_detail(request,paramm):
	v_customer = Customer.objects.filter(id=paramm).annotate(num_oppty=Count('preproject'))
	v_preproject = Preproject.objects.filter(customer__id=paramm)
	return render(request, 'customerdetail.html',{
	'p_list': v_preproject,
	'c_list': v_customer,
	})