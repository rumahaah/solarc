from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from . models import Preproject, Customer
from psatopca.models import Psa, Pca


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

def exclude_preproprogres ():
	my_list = []
	for preproject in Preproject.objects.all():
		my_list.append(preproject.id)
	for preproject in Preproject.objects.filter(progress='s'):
		my_list.remove(preproject.id)
	for preproject in Preproject.objects.filter(progress='p'):
		my_list.remove(preproject.id)
	return my_list

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
		v_preproject = Preproject.objects.all()
	elif paramm == 'progresssa':
		# b = preproprogres()
		v_preproject = Preproject.objects.filter(progress='p')
		# v_preproject = Preproject.objects.filter(pk__in=preproprogres())
		# v_preproject = Preproject.objects.filter(progress='s').filter(progress='p')
		# v_preproject = Preproject.objects.filter(preproject__progress_contains='s')
		# v_psa = Psa.objects.filter(status_psa='g').order_by(Lower('psa_date').desc())
	elif paramm == 'submited':
		v_preproject = Preproject.objects.filter(progress='s')

	elif paramm == 'closewon':
		v_preproject = Preproject.objects.filter(progress='w')

	elif paramm == 'closelost':
		v_preproject = Preproject.objects.filter(progress='l')

	elif paramm == 'exprogress':
		v_preproject = Preproject.objects.filter(pk__in=exclude_preproprogres())
	else:
		v_preproject =''

	return render(request, 'preproject.html',{
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
def detail (request,paramm='all'):
	if paramm == 'n':
		v_list = Preproject.objects.filter(sa_lintasarta__initial='')
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
	})


@login_required
def customer_list(request):
	# v_customer = Customer.objects.order_by(Lower('customer_criteria'))
	my_list = []
	for customer in Customer.objects.filter(customer_criteria='0'):
		my_list.append(customer.id)
	for customer in Customer.objects.filter(customer_criteria='1'):
		my_list.append(customer.id)

	v_customer = Customer.objects.filter(pk__in=my_list).order_by(Lower('customer_criteria'))
	return render(request, 'customer.html',{
	'list': v_customer,
	})