from datetime import datetime
import numpy
import statistics 

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower, Coalesce
from django.db.models import Avg, Sum, Value
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse

from . models import Psa, Pca
from preproject.models import Othersperson
from . filters import Psafilter, Pcafilter

# Create your views here.

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
		pcas = psa.pca_set.all()
		# pcas = psa.pca_set.exclude(psa__pss_ho_date__isnull=True)
		calculation = numpy.busday_count(psa.psa_date,datetime.now().date())
		if calculation >= 5:
			my_list.append(psa.id)
		for pca in pcas:
			if psa.pss_ho_date is None:
				''
			else:
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
def sendemail(request, pk=None):
	jmsa1 = Othersperson.objects.get(flag='1').email
	jmsa2 = Othersperson.objects.get(flag='2').email
	smpss = Othersperson.objects.get(flag='3').email
	smsa = Othersperson.objects.get(flag='4').email
	flagsendemail = Psa.objects.get(pk=pk).flagsendemail
	datapsa = Psa.objects.filter(pk=pk)
	for psa in datapsa:
		salesemail = psa.preproject.sales_lintasarta.email
		projectname = psa.preproject.project_name
		preprojectid = psa.preproject.id
		for customer in psa.preproject.customer.all():
			customer_name = customer.customer_name
		for pss in psa.preproject.pss_lintasarta.all():
			pssemail = pss.email
		for sa in psa.preproject.sa_lintasarta.all():
			saemail = sa.email
			sasubbag = sa.subbag
	if sasubbag == '1':
		jmemail = jmsa1
	elif sasubbag == '2':
		jmemail = jmsa2
	else:
		jmemail = ''

	subject = 'Handover PSS to SA - %s' % (projectname)
	from_email = 'Solution Architect <solarc.solutionarchitect@gmail.com>'
	context = {'datapsa': datapsa,}
	to = [salesemail,pssemail,saemail,]
	# to = ['solarc.solutionarchitect@gmail.com',]
	cc = [jmemail,smpss,smsa,]
	# reply_to= to + cc
	reply_to= [salesemail,pssemail,saemail,jmemail,smpss,smsa,]
	if saemail == 'tbc@tbc.tbc':
		return render(request, 'respond_email.html',{'message': '<span class="uk-text-danger">Failed.</span> Assign SA first (<a href="/admin/preproject/preproject/%s/change/">click</a>) before  sending an email. <br>Project %s and customer %s.' % (preprojectid,projectname,customer_name)})
	elif subject and from_email and to and cc and flagsendemail==0:
	# elif subject and from_email and to and flagsendemail==0:
	# elif subject and from_email and to:
		try:
			msg_html = render_to_string('sendemail.html',context)
			msg = EmailMessage(subject=subject, body=msg_html, from_email=from_email, to=to, cc=cc, reply_to=reply_to)
			# msg = EmailMessage(subject=subject, body=msg_html, from_email=from_email, to=to, reply_to=reply_to)
			msg.content_subtype = "html"  # Main content is now text/html
			msg.send()
			Psa.objects.filter(pk=pk).update(flagsendemail=1)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return render(request, 'respond_email.html',{'message': 'The email was sent <span class="uk-text-success">successfully</span>. <br>Project %s and customer %s.' % (projectname,customer_name)})
		# return HttpResponseRedirect('%s%s' % ('/sendemail/cc/',pk))
	else:
		return render(request, 'respond_email.html',{'message': '<span class="uk-text-danger">Failed.</span> An email has been sent before. <br>Project %s and customer %s.' % (projectname,customer_name)})

@login_required
def index_psa (request,paramm='total',idpsa=None):
	if paramm == 'total':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.order_by(Lower('psa_date').desc()))
	elif paramm == 'totalsa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(preproject__sa_lintasarta__subbag='1').order_by(Lower('psa_date').desc()))
	elif paramm == 'totalsa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(preproject__sa_lintasarta__subbag='2').order_by(Lower('psa_date').desc()))
	elif paramm == 'go':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(status_psa='g').order_by(Lower('psa_date').desc()))
	elif paramm == 'gosa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta__subbag='1').order_by(Lower('psa_date').desc()))
	elif paramm == 'gosa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta__subbag='2').order_by(Lower('psa_date').desc()))
	elif paramm == 'not':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.exclude(status_psa='g').order_by(Lower('psa_date').desc()))
	elif paramm == 'notsa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.exclude(status_psa='g').filter(preproject__sa_lintasarta__subbag='1').order_by(Lower('psa_date').desc()))
	elif paramm == 'notsa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.exclude(status_psa='g').filter(preproject__sa_lintasarta__subbag='2').order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wd':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdsa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd(Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta__subbag='1').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdsa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd(Psa.objects.filter(status_psa='g').filter(preproject__sa_lintasarta__subbag='2').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpssho':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpsshosa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c'))).filter(preproject__sa_lintasarta__subbag='1').order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpsshosa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c'))).filter(preproject__sa_lintasarta__subbag='2').order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpssho-sa1':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(sub_dept='sa1').filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	elif paramm == 'psa5wdpssho-sa2':
		v_psa = Psafilter(request.GET, queryset=Psa.objects.filter(pk__in=psa_more_than_5wd_from_pss_ho(Psa.objects.filter(sub_dept='sa2').filter(status_psa='g').exclude(preproject__progress='c'))).order_by(Lower('psa_date').desc()))
	else:
		v_psa = ''
	return render(request, 'psa.html',{
	# return render(request, 'psa_oioi.html',{
		'list': v_psa,
		'idpsa': idpsa,
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.order_by(Lower('pca_date').desc()))
	elif paramm == 'totalsa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('pca_date').desc()))
	elif paramm == 'totalsa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('pca_date').desc()))
	elif paramm == 'go':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(status_pca='g').order_by(Lower('pca_date').desc()))
	elif paramm == 'gosa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('pca_date').desc()))
	elif paramm == 'gosa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('pca_date').desc()))
	elif paramm == 'not':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(status_pca='g').order_by(Lower('pca_date').desc()))
	elif paramm == 'notsa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('pca_date').desc()))
	elif paramm == 'notsa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('pca_date').desc()))
	elif paramm == 'pca21wd':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=progressafterpca_21days(Pca.objects.filter(status_pca='g'))).order_by(Lower('pca_date').desc()))
	elif paramm == 'pca21wdsa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=progressafterpca_21days(Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='1'))).order_by(Lower('pca_date').desc()))
	elif paramm == 'pca21wdsa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=progressafterpca_21days(Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='2'))).order_by(Lower('pca_date').desc()))
	elif paramm == 'pcaebitda':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').filter(flagcalc=1).order_by(Lower('pca_date').desc()))
	elif paramm == 'pcaebitdasa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').filter(flagcalc=1).filter(psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('pca_date').desc()))
	elif paramm == 'pcaebitdasa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').filter(flagcalc=1).filter(psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('pca_date').desc()))
	elif paramm == 'pcairr':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').filter(flagcalc=1).order_by(Lower('pca_date').desc()))
	elif paramm == 'pcairrsa1':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').filter(flagcalc=1).filter(psa__preproject__sa_lintasarta__subbag='1').order_by(Lower('pca_date').desc()))
	elif paramm == 'pcairrsa2':
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').filter(flagcalc=1).filter(psa__preproject__sa_lintasarta__subbag='2').order_by(Lower('pca_date').desc()))
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=my_list_winlost).filter(flagcalc=1))
	elif paramm == 'pcaksaeasa1':
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').filter(pk__in=my_list_winlost).filter(flagcalc=1))
	elif paramm == 'pcaksaeasa2':
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').filter(pk__in=my_list_winlost).filter(flagcalc=1))
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(pk__in=my_list_winlost).filter(flagcalc=1))
	elif paramm == 'pcanonksaeasa1':
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').filter(pk__in=my_list_winlost).filter(flagcalc=1))
	elif paramm == 'pcanonksaeasa2':
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
		v_pca = Pcafilter(request.GET, queryset=Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').filter(pk__in=my_list_winlost).filter(flagcalc=1))
	else:
		v_psa = ''

	return render(request, 'pca.html',{
	# return render(request, 'pcawin.html',{
		'list': v_pca,
		})

# def ebitdaprofitability():
# 	avgebitda = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').aggregate(Avg('ebitda'))
# 	datas = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').values_list('duration','otc','mrc','ebitda')
# 	sum_tcv = sum(data[0] * data[2] + data[1] for data in datas)
# 	sum_ebitda_weighted = 0
# 	for data in datas:
# 		weighted = ((data[0] * data[2]) + data[1]) / sum_tcv
# 		ebitda_weighted = data[3] * weighted
# 		sum_ebitda_weighted += ebitda_weighted
# 	return [round(avgebitda['ebitda__avg'],1), round(sum_ebitda_weighted,1)]

def ebitdaprofitability(query):
	# avgebitda = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').filter(flagcalc=1).aggregate(Avg('ebitda'))
	avgebitda = query.aggregate(Avg('ebitda'))
	# sum_tcv = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').aggregate(the_sum=Coalesce(Sum('tcv'), Value(0)))['the_sum']
	# datas = Pca.objects.exclude(ebitda=0).filter(psa__preproject__progress='w').filter(flagcalc=1).values_list('tcv','ebitda')
	datas = query.values_list('tcv','ebitda')
	sum_tcv = sum(data[0] for data in datas)
	sum_ebitda_weighted = 0
	for pca in datas:
		weighted = pca[0] / sum_tcv
		ebitda_weighted = pca[1] * weighted
		sum_ebitda_weighted += ebitda_weighted
	return [round(avgebitda['ebitda__avg'],1), round(sum_ebitda_weighted,1)]

# def irrprofitability():
# 	avgirr = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').aggregate(Avg('irr'))
# 	datas = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').values_list('duration','otc','mrc','irr')
# 	sum_tcv = sum(data[0] * data[2] + data[1] for data in datas)
# 	sum_irr_weighted = 0
# 	for data in datas:
# 		weighted = ((data[0] * data[2]) + data[1]) / sum_tcv
# 		irr_weighted = data[3] * weighted
# 		sum_irr_weighted += irr_weighted
# 	return [round(avgirr['irr__avg'],1), round(sum_irr_weighted,1)]

def irrprofitability(query):
	# avgirr = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').filter(flagcalc=1).aggregate(Avg('irr'))
	avgirr = query.aggregate(Avg('irr'))
	# datas = Pca.objects.exclude(irr=0).filter(psa__preproject__progress='w').filter(flagcalc=1).values_list('tcv','irr')
	datas = query.values_list('tcv','irr')
	sum_tcv = sum(data[0] for data in datas)
	sum_irr_weighted = 0
	for pca in datas:
		weighted = pca[0] / sum_tcv
		irr_weighted = pca[1] * weighted
		sum_irr_weighted += irr_weighted
	return [round(avgirr['irr__avg'],1), round(sum_irr_weighted,1)]

# def winrate_ksaea():
# 	my_list = []
# 	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
# 		my_list.append(str(pca.id))
# 	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
# 		my_list.append(str(pca.id))
# 	list_ksaea_won = Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='w').values_list('duration','otc','mrc')
# 	list_ksaea_lost = Pca.objects.filter(pk__in=my_list).filter(psa__preproject__progress='l').values_list('duration','otc','mrc')
# 	sum_tcv_won = sum(data[0] * data[2] + data[1] for data in list_ksaea_won)
# 	sum_tcv_lost = sum(data[0] * data[2] + data[1] for data in list_ksaea_lost)
# 	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
# 	return [round(winrate,1), sum_tcv_won, sum_tcv_lost]

def winrate_ksaea(query):
	# my_list = []
	# for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
	# 	my_list.append(str(pca.id))
	# for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
	# 	my_list.append(str(pca.id))
	list_ksaea_won = query.filter(psa__preproject__customer__customer_criteria='0').filter(psa__preproject__progress='w').filter(flagcalc=1).values_list('tcv') | query.filter(psa__preproject__customer__customer_criteria='1').filter(psa__preproject__progress='w').filter(flagcalc=1).values_list('tcv')
	list_ksaea_lost = query.filter(psa__preproject__customer__customer_criteria='0').filter(psa__preproject__progress='l').filter(flagcalc=1).values_list('tcv') | query.filter(psa__preproject__customer__customer_criteria='1').filter(psa__preproject__progress='l').filter(flagcalc=1).values_list('tcv')
	list_ksaea_progress_submited = query.filter(psa__preproject__customer__customer_criteria='0').filter(psa__preproject__progress='p').filter(flagcalc=1).values_list('tcv') | query.filter(psa__preproject__customer__customer_criteria='1').filter(psa__preproject__progress='p').filter(flagcalc=1).values_list('tcv') | query.filter(psa__preproject__customer__customer_criteria='0').filter(psa__preproject__progress='s').filter(flagcalc=1).values_list('tcv') | query.filter(psa__preproject__customer__customer_criteria='1').filter(psa__preproject__progress='s').filter(flagcalc=1).values_list('tcv')
	sum_tcv_won = sum(data[0] for data in list_ksaea_won)
	sum_tcv_lost = sum(data[0] for data in list_ksaea_lost)
	sum_tcv_progress_submited = sum(data[0] for data in list_ksaea_progress_submited)
	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
	return [round(winrate,1), sum_tcv_won, sum_tcv_lost, sum_tcv_progress_submited]

# def winrate_nonksaea():
# 	my_list = []
# 	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
# 		my_list.append(str(pca.id))
# 	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
# 		my_list.append(str(pca.id))
# 	list_ksaea_won = Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='w').values_list('duration','otc','mrc')
# 	list_ksaea_lost = Pca.objects.exclude(pk__in=my_list).filter(psa__preproject__progress='l').values_list('duration','otc','mrc')
# 	sum_tcv_won = sum(data[0] * data[2] + data[1] for data in list_ksaea_won)
# 	sum_tcv_lost = sum(data[0] * data[2] + data[1] for data in list_ksaea_lost)
# 	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
# 	return [round(winrate,1), sum_tcv_won, sum_tcv_lost]

def winrate_nonksaea(query):
	my_list = []
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='0'):
		my_list.append(str(pca.id))
	for pca in Pca.objects.filter(psa__preproject__customer__customer_criteria='1'):
		my_list.append(str(pca.id))
	list_nonksaea_won = query.exclude(pk__in=my_list).filter(psa__preproject__progress='w').filter(flagcalc=1).values_list('tcv')
	list_nonksaea_lost = query.exclude(pk__in=my_list).filter(psa__preproject__progress='l').filter(flagcalc=1).values_list('tcv')
	list_nonksaea_progress_submited = query.exclude(pk__in=my_list).filter(psa__preproject__progress='p').filter(flagcalc=1).values_list('tcv') | query.exclude(pk__in=my_list).filter(psa__preproject__progress='s').filter(flagcalc=1).values_list('tcv')
	sum_tcv_won = sum(data[0] for data in list_nonksaea_won)
	sum_tcv_lost = sum(data[0] for data in list_nonksaea_lost)
	sum_tcv_progress_submited = sum(data[0] for data in list_nonksaea_progress_submited)
	winrate = sum_tcv_won / (sum_tcv_won + sum_tcv_lost) *100
	return [round(winrate,1), sum_tcv_won, sum_tcv_lost, sum_tcv_progress_submited]

def risk_criteria():
	hr = Psa.objects.filter(risk_category='h')
	mr = Psa.objects.filter(risk_category='m')
	lr = Psa.objects.filter(risk_category='l')
	return [hr,mr,lr]