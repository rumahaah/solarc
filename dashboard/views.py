from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from psatopca.models import Psa, Pca
from handover.models import Handover
from preproject.models import Preproject
from psatopca.views import psa_more_than_5wd, psa_more_than_5wd_from_pss_ho, progressafterpca_21days, ebitdaprofitability, irrprofitability, winrate_ksaea, winrate_nonksaea, risk_criteria
from handover.views import ho_more_than_2wd_from_po_known_date
from preproject.views import exclude_preproprogres, oppty_per_customer

# from datetime import datetime
# import numpy

# Create your views here.
def home(request):
	return render(request, 'home_solarc.html')

@login_required
def about(request):
	return render(request, 'about_solarc.html')

# def psa_more_than_5wd (rawdata):
# 	my_list = []
# 	for data in rawdata:
# 		# psa_date = data.psa_date
# 		# pcas = data.pca_set.all()
# 		# for data in pcas:
# 		calculation = numpy.busday_count(data.psa_date,datetime.now().date())
# 		if calculation >= 5:
# 			psamorethan5wd = data.id
# 			my_list.append(str(psamorethan5wd))
# 	return my_list

# def psa_more_than_5wd (rawdata):
# 	my_list = []
# 	for psa in rawdata:
# 		# psa_date = psa.psa_date
# 		pcas = psa.pca_set.all()
# 		calculation = numpy.busday_count(psa.psa_date,datetime.now().date())
# 		if calculation >= 5:
# 			psamorethan5wd = psa.id
# 			my_list.append(str(psamorethan5wd))
# 		for pca in pcas:
# 			# check =  pca.pca_date - psa.psa_date
# 			check = numpy.busday_count(psa.psa_date,pca.pca_date)
# 			# if check.days <= 5:
# 			if check <= 5:
# 				psawaspca = pca.psa_id
# 				my_list.remove(str(psawaspca))
# 	return my_list

# def psa_more_than_5wd_from_pss_ho (rawdata):
# 	my_list = []
# 	for psa in rawdata:
# 		# psa_date = psa.psa_date
# 		pcas = psa.pca_set.all()
# 		calculation = numpy.busday_count(psa.psa_date,datetime.now().date())
# 		if calculation >= 5:
# 			psamorethan5wd = psa.id
# 			my_list.append(str(psamorethan5wd))
# 		for pca in pcas:
# 			# check =  pca.pca_date - psa.pss_ho_date
# 			check = numpy.busday_count(psa.pss_ho_date,pca.pca_date)
# 			# if check.days <= 5:
# 			if check <= 5:
# 				psawaspca = pca.psa_id
# 				my_list.remove(str(psawaspca))
# 	return my_list

# def ho_more_than_2wd_from_po_date(rawdata):
# 	my_list = []
# 	for handover in rawdata:
# 		check = numpy.busday_count(handover.po_date,datetime.now().date())
# 		if check >= 2:
# 			powas2wd = handover.id
# 			my_list.append(str(powas2wd))
# 	return my_list

# def ho_more_than_2wd_from_po_known_date(rawdata):
# 	my_list = []
# 	for handover in rawdata:
# 		check = numpy.busday_count(handover.po_known_date,datetime.now().date())
# 		if check >= 2:
# 			powas2wd = handover.id
# 			my_list.append(str(powas2wd))
# 	return my_list

@login_required
def dashboard_home(request):
	v_total_psa = Psa.objects.count()
	v_psa_go = Psa.objects.filter(status_psa='g').count()
	v_psa_holdnogo = Psa.objects.exclude(status_psa='g').count()
	v_total_pca = Pca.objects.count()
	v_pca_go = Pca.objects.filter(status_pca='g').count()
	v_pca_holdnogo = Pca.objects.exclude(status_pca='g').count()
	v_handover = Handover.objects.count()
	v_total_prepro = Preproject.objects.count()
	v_progress_prepro = Preproject.objects.filter(progress='p').count()
	v_submit_prepro = Preproject.objects.filter(progress='s').count()
	v_won_prepro = Preproject.objects.filter(progress='w').count()
	v_lost_prepro = Preproject.objects.filter(progress='l').count()
	# v_progress_prepro = len(preproprogres())
	v_exclude_progress_prepro = len(exclude_preproprogres())
	v_len_psa_more_than_5wd = len(psa_more_than_5wd(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')))
	# v_len_psa_more_than_5wd = len(psa_more_than_5wd(Psa.objects.all())[0])
	v_len_psa_more_than_5wd_from_pss_ho = len(psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')))
	v_len_progressafterpca_21days = len(progressafterpca_21days(Pca.objects.filter(status_pca='g')))
	v_len_ho_more_than_2wd_from_po_known_date = len(ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(problem_category='n-pr')))
	# v_len_ho_more_than_2wd_from_po_known_date = len(ho_more_than_2wd_from_po_known_date(Handover.objects.all()))

	#CHART
	v_total_psa_1 = Psa.objects.filter(psa_date__month='1').count()
	v_total_psa_2 = Psa.objects.filter(psa_date__month='2').count()
	v_total_psa_3 = Psa.objects.filter(psa_date__month='3').count()
	v_total_psa_4 = Psa.objects.filter(psa_date__month='4').count()
	v_total_psa_5 = Psa.objects.filter(psa_date__month='5').count()
	v_total_psa_6 = Psa.objects.filter(psa_date__month='6').count()
	v_total_psa_7 = Psa.objects.filter(psa_date__month='7').count()
	v_total_psa_8 = Psa.objects.filter(psa_date__month='8').count()
	v_total_psa_9 = Psa.objects.filter(psa_date__month='9').count()
	v_total_psa_10 = Psa.objects.filter(psa_date__month='10').count()
	v_total_psa_11 = Psa.objects.filter(psa_date__month='11').count()
	v_total_psa_12 = Psa.objects.filter(psa_date__month='12').count()

	v_total_pca_1 = Pca.objects.filter(pca_date__month='1').count()
	v_total_pca_2 = Pca.objects.filter(pca_date__month='2').count()
	v_total_pca_3 = Pca.objects.filter(pca_date__month='3').count()
	v_total_pca_4 = Pca.objects.filter(pca_date__month='4').count()
	v_total_pca_5 = Pca.objects.filter(pca_date__month='5').count()
	v_total_pca_6 = Pca.objects.filter(pca_date__month='6').count()
	v_total_pca_7 = Pca.objects.filter(pca_date__month='7').count()
	v_total_pca_8 = Pca.objects.filter(pca_date__month='8').count()
	v_total_pca_9 = Pca.objects.filter(pca_date__month='9').count()
	v_total_pca_10 = Pca.objects.filter(pca_date__month='10').count()
	v_total_pca_11 = Pca.objects.filter(pca_date__month='11').count()
	v_total_pca_12 = Pca.objects.filter(pca_date__month='12').count()

	# avgebitda, total_tcv = ebitdaprofitability()

	return render(request, 'dashboard_home.html',{
		# 'oi': psa_more_than_5wd(Psa.objects.all())[0],
		# 'oioi': psa_more_than_5wd(Psa.objects.all())[1],
		# 'oioioi': psa_more_than_5wd(Psa.objects.all())[2],
		'total_psas': v_total_psa,
		'go_psas': v_psa_go,
		'holdnotgo_psas': v_psa_holdnogo,
		'total_pcas': v_total_pca,
		'go_pcas': v_pca_go,
		'holdnotgo_pcas': v_pca_holdnogo,
		'handover': v_handover,
		'total_prepro': v_total_prepro,
		'progress_prepro': v_progress_prepro,
		'won_prepro': v_won_prepro,
		'lost_prepro': v_lost_prepro,
		'submit_prepro': v_submit_prepro,
		'exclude_progress_prepro': v_exclude_progress_prepro,
		'len_psa_more_than_5wd': v_len_psa_more_than_5wd,
		'len_psa_more_than_5wd_from_pss_ho': v_len_psa_more_than_5wd_from_pss_ho,
		'len_progressafterpca_21days': v_len_progressafterpca_21days,
		'len_ho_more_than_2wd_from_po_known_date': v_len_ho_more_than_2wd_from_po_known_date,
		'ebitdaprofitability': ebitdaprofitability()[0],
		'ebitdaprofitability_weighted': ebitdaprofitability()[1],
		'irrprofitability': irrprofitability()[0],
		'irrprofitability_weighted': irrprofitability()[1],
		'winrate_ksaea': winrate_ksaea()[0],
		'sum_tcv_won': winrate_ksaea()[1],
		'sum_tcv_lost': winrate_ksaea()[2],
		'winrate_nonksaea': winrate_nonksaea()[0],
		
		#CHART1 PSA & PCA
		'total_psa_1': v_total_psa_1,
		'total_psa_2': v_total_psa_2,
		'total_psa_3': v_total_psa_3,
		'total_psa_4': v_total_psa_4,
		'total_psa_5': v_total_psa_5,
		'total_psa_6': v_total_psa_6,
		'total_psa_7': v_total_psa_7,
		'total_psa_8': v_total_psa_8,
		'total_psa_9': v_total_psa_9,
		'total_psa_10': v_total_psa_10,
		'total_psa_11': v_total_psa_11,
		'total_psa_12': v_total_psa_12,
		'total_pca_1': v_total_pca_1,
		'total_pca_2': v_total_pca_2,
		'total_pca_3': v_total_pca_3,
		'total_pca_4': v_total_pca_4,
		'total_pca_5': v_total_pca_5,
		'total_pca_6': v_total_pca_6,
		'total_pca_7': v_total_pca_7,
		'total_pca_8': v_total_pca_8,
		'total_pca_9': v_total_pca_9,
		'total_pca_10': v_total_pca_10,
		'total_pca_11': v_total_pca_11,
		'total_pca_12': v_total_pca_12,

		#CHART3 Customer Criteria
		'qty_ksa': oppty_per_customer()[0],
		'qty_ea': oppty_per_customer()[1],
		'qty_sa': oppty_per_customer()[2],
		'qty_others': oppty_per_customer()[3],

		#CHART3 Risk Criteria
		'hr': risk_criteria()[0].count(),
		'mr': risk_criteria()[1].count(),
		'lr': risk_criteria()[2].count(),
		})

