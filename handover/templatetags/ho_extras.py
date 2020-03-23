from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.simple_tag
def totalcontracvalue(mrc, otc, duration, *args, **kwargs):
	# you would need to do any localization of the result here
	tcv = ( mrc * duration ) + otc
	if tcv:
		tcv = round(float(tcv), 2)
		return "Rp %s%s" % (intcomma(int(tcv)), ("%0.2f" % tcv)[-3:])
	else:
		return ''
	return tcv

@register.simple_tag
def annualcontracvalue(mrc, otc, *args, **kwargs):
	# you would need to do any localization of the result here
	acv = ( mrc * 12 ) + otc
	if acv:
		acv = round(float(acv), 2)
		return "Rp %s%s" % (intcomma(int(acv)), ("%0.2f" % acv)[-3:])
	else:
		return ''
	return acv