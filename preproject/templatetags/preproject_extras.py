from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.simple_tag
def rupiah(rupiah, *args, **kwargs):
	if rupiah:
		rupiah = round(float(rupiah), 2)
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
def annualcontracvalue(mrc, otc, month, *args, **kwargs):
	# you would need to do any localization of the result here
	if month == '1':
		month_num = 1
	elif month == '2':
		month_num = 2
	elif month == '3':
		month_num = 3
	elif month == '4':
		month_num = 4
	elif month == '5':
		month_num = 5
	elif month == '6':
		month_num = 6
	elif month == '7':
		month_num = 7
	elif month == '8':
		month_num = 8
	elif month == '9':
		month_num = 9
	elif month == '10':
		month_num = 10
	elif month == '11':
		month_num = 11
	else:
		month_num = 12

	duration = (12-month_num)+1

	acv = ( mrc * duration) + otc
	if acv:
		acv = round(float(acv), 2)
		return "%s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
	else:
		return ''
	return acv
	# return "%s - %s" % (acv,duration)
