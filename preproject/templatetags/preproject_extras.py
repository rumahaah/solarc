from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models.functions import Lower
from datetime import datetime
from psatopca.models import Psa, Pca, Preproject

register = template.Library()

@register.simple_tag
def rupiah(rupiah, *args, **kwargs):
	if rupiah:
		# rupiah = round(float(rupiah), 2)
		return "%s%s" % (intcomma(int(rupiah)), ("%0.2f" % rupiah)[-3:])
	else:
		return 0
	return rupiah

@register.simple_tag
def totalcontracvalue(mrc, otc, duration, *args, **kwargs):
	# you would need to do any localization of the result here
	tcv = ( mrc * duration ) + otc
	if tcv:
		tcv = round(float(tcv), 2)
		return "%s%s" % (intcomma(int(tcv)), ("%0.2f" % tcv)[-3:])
	else:
		return ''
	return tcv

@register.simple_tag
def annualcontracvalue(pcaid, date, *args, **kwargs):
	# you would need to do any localization of the result here
	datestr = str(date)

	if datestr[:2] == '01':
		month_num = 1
	elif datestr[:2] == '02':
		month_num = 2
	elif datestr[:2] == '03':
		month_num = 3
	elif datestr[:2] == '04':
		month_num = 4
	elif datestr[:2] == '05':
		month_num = 5
	elif datestr[:2] == '06':
		month_num = 6
	elif datestr[:2] == '07':
		month_num = 7
	elif datestr[:2] == '08':
		month_num = 8
	elif datestr[:2] == '09':
		month_num = 9
	elif datestr[:2] == '10':
		month_num = 10
	elif datestr[:2] == '11':
		month_num = 11
	elif datestr[:2] == '12':
		month_num = 12
	else:
		month_num = 0

	# for pca in Pca.objects.filter(pk__in=pcaid):
	mrc = Pca.objects.get(id=pcaid).mrc
	otc = Pca.objects.get(id=pcaid).otc
	tcv = Pca.objects.get(id=pcaid).tcv

	duration = (12-month_num)+1

	if datestr[2:6] == '2020':
		acv = ( mrc * duration ) + otc
	elif datestr[2:6] == '2019':
		acv = ( mrc * 12 ) + otc
	else:
		acv = 10

	if tcv == 0:
		acv = round(float(acv), 2)
		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
	elif acv >= tcv:
		acv = round(float(tcv), 2)
		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
	elif acv < tcv:
		acv = round(float(acv), 2)
		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
	else:
		acv = round(float(acv), 2)
		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])

	return acv

# @register.simple_tag
# def annualcontracvalue(mrc, otc, date, *args, **kwargs):
# 	# you would need to do any localization of the result here
# 	datestr = str(date)

# 	if datestr[:2] == '01':
# 		month_num = 1
# 	elif datestr[:2] == '02':
# 		month_num = 2
# 	elif datestr[:2] == '03':
# 		month_num = 3
# 	elif datestr[:2] == '04':
# 		month_num = 4
# 	elif datestr[:2] == '05':
# 		month_num = 5
# 	elif datestr[:2] == '06':
# 		month_num = 6
# 	elif datestr[:2] == '07':
# 		month_num = 7
# 	elif datestr[:2] == '08':
# 		month_num = 8
# 	elif datestr[:2] == '09':
# 		month_num = 9
# 	elif datestr[:2] == '10':
# 		month_num = 10
# 	elif datestr[:2] == '11':
# 		month_num = 11
# 	elif datestr[:2] == '12':
# 		month_num = 12
# 	else:
# 		month_num = 0

# 	duration = (12-month_num)+1

# 	if datestr[2:6] == '2020':
# 		acv = ( mrc * duration) + otc
# 	elif datestr[2:6] == '2019':
# 		acv = ( mrc * 12) + otc
# 	else:
# 		acv = 10

# 	if acv:
# 		acv = round(float(acv), 2)
# 		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
# 	else:
# 		return ''
# 	return acv

# @register.simple_tag
# def annualcontracvalue(mrc, otc, month, *args, **kwargs):
# 		# you would need to do any localization of the result here
# 		if month == '1':
# 			month_num = 1
# 		elif month == '2':
# 			month_num = 2
# 		elif month == '3':
# 			month_num = 3
# 		elif month == '4':
# 			month_num = 4
# 		elif month == '5':
# 			month_num = 5
# 		elif month == '6':
# 			month_num = 6
# 		elif month == '7':
# 			month_num = 7
# 		elif month == '8':
# 			month_num = 8
# 		elif month == '9':
# 			month_num = 9
# 		elif month == '10':
# 			month_num = 10
# 		elif month == '11':
# 			month_num = 11
# 		else:
# 			month_num = 12

# 		duration = (12-month_num)+1

# 		acv = ( mrc * duration) + otc
# 		if acv:
# 			acv = round(float(acv), 2)
# 			return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
# 		else:
# 			return ''
# 		return acv
# 		# return "%s - %s" % (acv,duration)

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

# @register.simple_tag
# def pcadate(pcaid, *args, **kwargs):
# 	# pcadate = Pca.objects.get(id=pcaid).pca_date
# 	# pcadate = Pca.objects.filter(id=pcaid).latest('pca_date').pca_date
# 	# pcadate = Pca.objects.filter(id=pcaid).latest('pca_date', '-pca_date').pca_date
# 	# pcadate = Pca.objects.filter(id=pcaid).order_by('pca_date').last().pca_date
# 	pcadate = Pca.objects.filter(id=pcaid).order_by('-pca_date')[0].pca_date
# 	# pcas = Pca.objects.filter(id=pcaid).order_by(Lower('pca_date').desc())
# 	# pcas = Pca.objects.filter(id=pcaid).latest('pca_date')
# 	# pcas = Pca.objects.filter(id=pcaid)
# 	# for pca in pcas:
# 		# pcadate = pca.pca_date
# 	return pcadate

@register.simple_tag
def psa_data(preprojectid):
	try:
		psa_data = Psa.objects.filter(preproject__id=preprojectid).latest('psa_date')
	except:
		psa_data = ''
	return psa_data

@register.simple_tag
def pca_data(preprojectid):
	# pca_data = Pca.objects.filter(psa__preproject__id=preprojectid).latest('pca_date')
	try:
		pca_data = Pca.objects.filter(psa__preproject__id=preprojectid).latest('pca_date')
	except:
		pca_data = ''
	return pca_data