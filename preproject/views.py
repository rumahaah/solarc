from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from . models import Preproject, Customer

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
	ksa = Preproject.objects.filter(oppty__customer__customer_criteria='0').count()
	ea = Preproject.objects.filter(oppty__customer__customer_criteria='1').count()
	sa = Preproject.objects.filter(oppty__customer__customer_criteria='2').count()
	x = Preproject.objects.filter(oppty__customer__customer_criteria='3').count()
	y = Preproject.objects.filter(oppty__customer__customer_criteria='4').count()
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
	return render(request, 'preproject_won.html',{
	'list': v_preproject,
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