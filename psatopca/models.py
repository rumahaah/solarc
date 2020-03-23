from django.db import models
from preproject.models import Preproject

# Create your models here.
class Psa(models.Model):
	preproject = models.ForeignKey('preproject.Preproject', on_delete=models.CASCADE)
	# product_category_option = (
	# 	('d', 'Datacomm'),
	# 	('i', 'ITS'),
	# )
	productornot_option = (
		('p', 'Product'),
		('n', 'Non Product'),
	)
	scale_option = (
		('s', 'Small'),
		('m', 'Medium'),
		('l', 'Large'),
	)
	status_option = (
		('g', 'GO'),
		('h', 'HOLD'),
		('n', 'NOT GO'),
	)
	risk_category_option = (
		('l', 'Low Risk'),
		('m', 'Medium Risk'),
		('h', 'High Risk'),
		('n', 'N/A'),
	)
	sub_dept_option = (
		('sa1', 'SA 1 Sub Dept'),
		('sa2', 'SA 2 Sub Dept'),
	)
	psa_date = models.DateField()
	pss_ho_date = models.DateField(blank=True, null=True)
	# pca_date = models.DateField(blank=True, null=True)
	# product_category =  models.CharField(max_length=1, choices=product_category_option)
	# customer = models.ManyToManyField('preproject.Customer')
	# customer = models.ForeignKey('preproject.Customer', on_delete=models.CASCADE)
	# customer = models.ForeignKey('Customer')
	# project_name = models.CharField(max_length=100)
	# sales_lintasarta = models.ForeignKey('preproject.Lintasartaperson',related_name='+', on_delete=models.CASCADE)
	# sales_lintasarta = models.ForeignKey('preproject.Lintasartaperson',related_name="Psapca.sales_lintasarta",on_delete=models.CASCADE)
	# pss_lintasarta = models.ManyToManyField('preproject.Lintasartaperson',related_name='+')
	# pss_lintasarta = models.ManyToManyField('preproject.Lintasartaperson',related_name="Psapca.pss_lintasarta")
	productornot =  models.CharField(max_length=1, choices=productornot_option)
	scale =  models.CharField(max_length=1, choices=scale_option)
	summary = models.TextField(max_length=1000)
	status_psa = models.CharField(max_length=1, choices=status_option)
	remark = models.TextField(max_length=1000, blank=True, null=True)
	attendance = models.TextField(max_length=1000, blank=True, null=True)
	risk_category = models.CharField(max_length=1, choices=risk_category_option)
	sub_dept = models.CharField(max_length=3, choices=sub_dept_option)
	
	#timestamp
	table_updated = models.DateField(auto_now=True, auto_now_add=False)
	table_creation_timestamp = models.DateField(auto_now=False, auto_now_add=True)

	# def is_upperclass(self):
	# 	return self.status_psa in {self.h, self.g}

	def __str__(self):
		if self.status_psa == 'g':
			status_psa_1 = 'PSA: GO'
		elif self.status_psa == 'h':
			status_psa_1 = 'PSA: HOLD'
		else:
			status_psa_1 = 'PSA: NOT GO'
		return "%s - %s " % (self.preproject, status_psa_1)

class Pca(models.Model):
	status_option = (
		('g', 'GO/APPROVED'),
		('h', 'HOLD'),
		('n', 'NOT GO'),
	)
	problem_category_option = (
		('n-pr','No Problem - Fulfilled'),
		('e-ra','External - Resource Assessment'),
		('e-sc','External - Scope Change'),
		('e-cb','External - Source Costbase'),
		('e-vc','External - Very Complex'),
		('i-so','Internal - Incorrect Solution'),
		('i-bp','Internal - Incorrect Price'),
	)
	psa = models.ForeignKey('Psa', on_delete=models.CASCADE)
	pca_date = models.DateField()
	status_pca = models.CharField(max_length=1, choices=status_option)
	otc = models.DecimalField(max_digits=30, decimal_places=2)
	mrc = models.DecimalField(max_digits=30, decimal_places=2)
	duration = models.IntegerField()
	ebitda = models.DecimalField(max_digits=10, decimal_places=2)
	irr = models.DecimalField(max_digits=10, decimal_places=2)
	remark = models.TextField(max_length=1000, blank=True, null=True)
	attendance = models.TextField(max_length=1000, blank=True, null=True)
	problem_category = models.CharField(max_length=4, choices=problem_category_option, default='n-pr')
	# problem_category = models.CharField(max_length=4, choices=problem_category_option)

	#timestamp
	table_updated = models.DateField(auto_now=True, auto_now_add=False)
	table_creation_timestamp = models.DateField(auto_now=False, auto_now_add=True)
	
	def __str__(self):
		if self.status_pca == 'g':
			status_pca_1 = 'PCA: APPROVED'
		elif self.status_pca == 'h':
			status_pca_1 = 'PCA: HOLD'
		else:
			status_pca_1 = 'PCA: NOT GO'
		return "%s - %s" % (self.psa, status_pca_1)