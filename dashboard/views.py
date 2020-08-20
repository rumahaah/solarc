from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from psatopca.models import Psa, Pca
from handover.models import Handover
from preproject.models import Preproject
from psatopca.views import psa_more_than_5wd, psa_more_than_5wd_from_pss_ho, progressafterpca_21days, ebitdaprofitability, irrprofitability, winrate_ksaea, winrate_nonksaea, risk_criteria
from handover.views import ho_more_than_2wd_from_po_known_date
from preproject.views import oppty_per_customer

# from datetime import datetime
# import numpy
from decimal import Decimal

# Create your views here.
def home(request):
	return render(request, 'home_solarc.html')

@login_required
def about(request):
	return render(request, 'about_solarc.html')

@login_required
def Dashboard(request):
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
	v_cancelled_psahold_prepro = Preproject.objects.filter(progress='c').count() + Preproject.objects.filter(progress='h').count()
	v_len_psa_more_than_5wd = len(psa_more_than_5wd(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')))
	v_len_psa_more_than_5wd_from_pss_ho = len(psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c')))
	v_len_progressafterpca_21days = len(progressafterpca_21days(Pca.objects.filter(status_pca='g')))
	v_len_ho_more_than_2wd_from_po_known_date = len(ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(clean_project_category='n-pr')))
	

	# ebitdaprofitability
	ebitdaprofitability_avg = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e'))[0]
	ebitdaprofitability_weighted = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e'))[1]
	ebitdaprofitability_weighted_otc_mrc_only = ebitdaprofitability(Pca.objects.filter(bc_category='o').exclude(psa__preproject__payment='m').filter(psa__preproject__progress='w').exclude(bc_category='e'))[1]
	ebitdaprofitability_weighted_mrc_only = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__payment='m').filter(psa__preproject__progress='w').exclude(bc_category='e'))[1]
	
	# irrprofitability_avg
	irrprofitability_avg = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').filter(psa__preproject__progress='w').exclude(bc_category='e'))[0]
	irrprofitability_weighted = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').exclude(bc_category='e'))[1]
	irrprofitability_weighted_ebitda = ebitdaprofitability(Pca.objects.exclude(ebitda=0).filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e'))[1]

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

	sum_tcv_won = (winrate_ksaea(Pca.objects)[1] + winrate_nonksaea(Pca.objects)[1]) / 1000000000
	sum_tcv_lost = (winrate_ksaea(Pca.objects)[2] + winrate_nonksaea(Pca.objects)[2]) / 1000000000
	sum_tcv_progress = (winrate_ksaea(Pca.objects)[3] + winrate_nonksaea(Pca.objects)[3]) / 1000000000


	return render(request, 'dashboard.html',{
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
		'cancelled_psahold_prepro': v_cancelled_psahold_prepro,
		'len_psa_more_than_5wd': v_len_psa_more_than_5wd,
		'len_psa_more_than_5wd_from_pss_ho': v_len_psa_more_than_5wd_from_pss_ho,
		'len_progressafterpca_21days': v_len_progressafterpca_21days,
		'len_ho_more_than_2wd_from_po_known_date': v_len_ho_more_than_2wd_from_po_known_date,
		'ebitdaprofitability_avg': ebitdaprofitability_avg,
		'ebitdaprofitability_weighted': ebitdaprofitability_weighted,
		'ebitdaprofitability_weighted_otc_mrc_only': ebitdaprofitability_weighted_otc_mrc_only,
		'ebitdaprofitability_weighted_mrc_only': ebitdaprofitability_weighted_mrc_only,
		'irrprofitability_avg': irrprofitability_avg,
		'irrprofitability_weighted': irrprofitability_weighted,
		'irrprofitability_weighted_ebitda': irrprofitability_weighted_ebitda,
		'winrate_ksaea': winrate_ksaea(Pca.objects)[0],
		'winrate_nonksaea': winrate_nonksaea(Pca.objects)[0],
		
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

		#CHART2 Revenue TCV (Plan)
		'sum_tcv_won': sum_tcv_won,
		'sum_tcv_lost': sum_tcv_lost,
		'sum_tcv_progress': sum_tcv_progress,


		#CHART3 Customer Criteria
		'qty_ksa': oppty_per_customer()[0],
		'qty_ea': oppty_per_customer()[1],
		'qty_sa': oppty_per_customer()[2],
		'qty_others': oppty_per_customer()[3],

		#CHART4 Risk Criteria
		'hr': risk_criteria()[0].count(),
		'mr': risk_criteria()[1].count(),
		'lr': risk_criteria()[2].count(),
	})

@login_required
def Dashboardsubbag(request,paramm='sa1'):
	if paramm == 'sa1':
		v_total_psa = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').count()
		v_psa_go = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').filter(status_psa='g').count()
		v_psa_holdnogo = Psa.objects.filter(preproject__sa_lintasarta__subbag='1').exclude(status_psa='g').count()
		v_total_pca = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').count()
		v_pca_go = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').filter(status_pca='g').count()
		v_pca_holdnogo = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1').exclude(status_pca='g').count()
		v_len_psa_more_than_5wd = len(psa_more_than_5wd(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta__subbag='1')))
		v_len_psa_more_than_5wd_from_pss_ho = len(psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta__subbag='1')))
		v_len_progressafterpca_21days = len(progressafterpca_21days(Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='1')))
		v_total_prepro = Preproject.objects.filter(sa_lintasarta__subbag='1').count()
		v_progress_prepro = Preproject.objects.filter(progress='p').filter(sa_lintasarta__subbag='1').count()
		v_submit_prepro = Preproject.objects.filter(progress='s').filter(sa_lintasarta__subbag='1').count()
		v_cancelled_psahold_prepro = Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='c').count() + Preproject.objects.filter(sa_lintasarta__subbag='1').filter(progress='h').count()
		v_won_prepro = Preproject.objects.filter(progress='w').filter(sa_lintasarta__subbag='1').count()
		v_lost_prepro = Preproject.objects.filter(progress='l').filter(sa_lintasarta__subbag='1').count()
		v_handover = Handover.objects.filter(pca__psa__preproject__sa_lintasarta__subbag='1').count()
		v_len_ho_more_than_2wd_from_po_known_date = len(ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(clean_project_category='n-pr').filter(pca__psa__preproject__sa_lintasarta__subbag='1')))



		ebitdaprofitability_avg = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='1'))[0]
		ebitdaprofitability_weighted = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='1'))[1]
		irrprofitability_avg = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='1'))[0]
		irrprofitability_weighted = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='1'))[1]
		v_winrate_ksaea = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1'))[0]
		v_sum_tcv_won = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1'))[1]
		v_sum_tcv_lost = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1'))[2]
		v_winrate_nonksaea = winrate_nonksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='1'))[0]

	elif paramm == 'sa2':
		v_total_psa = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').count()
		v_psa_go = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').filter(status_psa='g').count()
		v_psa_holdnogo = Psa.objects.filter(preproject__sa_lintasarta__subbag='2').exclude(status_psa='g').count()
		v_total_pca = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').count()
		v_pca_go = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').filter(status_pca='g').count()
		v_pca_holdnogo = Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2').exclude(status_pca='g').count()
		v_len_psa_more_than_5wd = len(psa_more_than_5wd(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta__subbag='2')))
		v_len_psa_more_than_5wd_from_pss_ho = len(psa_more_than_5wd_from_pss_ho(Psa.objects.filter(status_psa='g').exclude(preproject__progress='c').filter(preproject__sa_lintasarta__subbag='2')))
		v_len_progressafterpca_21days = len(progressafterpca_21days(Pca.objects.filter(status_pca='g').filter(psa__preproject__sa_lintasarta__subbag='2')))
		v_total_prepro = Preproject.objects.filter(sa_lintasarta__subbag='2').count()
		v_progress_prepro = Preproject.objects.filter(progress='p').filter(sa_lintasarta__subbag='2').count()
		v_submit_prepro = Preproject.objects.filter(progress='s').filter(sa_lintasarta__subbag='2').count()
		v_cancelled_psahold_prepro = Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='c').count() + Preproject.objects.filter(sa_lintasarta__subbag='2').filter(progress='h').count()
		v_won_prepro = Preproject.objects.filter(progress='w').filter(sa_lintasarta__subbag='2').count()
		v_lost_prepro = Preproject.objects.filter(progress='l').filter(sa_lintasarta__subbag='2').count()
		v_handover = Handover.objects.filter(pca__psa__preproject__sa_lintasarta__subbag='2').count()
		v_len_ho_more_than_2wd_from_po_known_date = len(ho_more_than_2wd_from_po_known_date(Handover.objects.exclude(clean_project_category='n-pr').filter(pca__psa__preproject__sa_lintasarta__subbag='2')))
	


		ebitdaprofitability_avg = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='2'))[0]
		ebitdaprofitability_weighted = ebitdaprofitability(Pca.objects.filter(bc_category='o').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='2'))[1]
		irrprofitability_avg = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='2'))[0]
		irrprofitability_weighted = irrprofitability(Pca.objects.filter(bc_category='c').filter(psa__preproject__progress='w').exclude(bc_category='e').filter(psa__preproject__sa_lintasarta__subbag='2'))[1]
		v_winrate_ksaea = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2'))[0]
		v_sum_tcv_won = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2'))[1]
		v_sum_tcv_lost = winrate_ksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2'))[2]
		v_winrate_nonksaea = winrate_nonksaea(Pca.objects.filter(psa__preproject__sa_lintasarta__subbag='2'))[0]

	return render(request, 'dashboard_subbag.html',{
		'total_psas': v_total_psa,
		'go_psas': v_psa_go,
		'holdnotgo_psas': v_psa_holdnogo,
		'total_pcas': v_total_pca,
		'go_pcas': v_pca_go,
		'holdnotgo_pcas': v_pca_holdnogo,
		'len_psa_more_than_5wd': v_len_psa_more_than_5wd,
		'len_psa_more_than_5wd_from_pss_ho': v_len_psa_more_than_5wd_from_pss_ho,
		'len_progressafterpca_21days': v_len_progressafterpca_21days,
		'total_prepro': v_total_prepro,
		'progress_prepro': v_progress_prepro,
		'submit_prepro': v_submit_prepro,
		'cancelled_psahold_prepro': v_cancelled_psahold_prepro,
		'won_prepro': v_won_prepro,
		'lost_prepro': v_lost_prepro,
		'handover': v_handover,
		'len_ho_more_than_2wd_from_po_known_date': v_len_ho_more_than_2wd_from_po_known_date,
		


		'ebitdaprofitability_avg': ebitdaprofitability_avg,
		'ebitdaprofitability_weighted': ebitdaprofitability_weighted,
		'irrprofitability_avg': irrprofitability_avg,
		'irrprofitability_weighted': irrprofitability_weighted,
		'subbag': paramm,
		'winrate_ksaea': v_winrate_ksaea,
		'sum_tcv_won': v_sum_tcv_won,
		'sum_tcv_lost': v_sum_tcv_lost,
		'winrate_nonksaea': v_winrate_nonksaea,

	})



