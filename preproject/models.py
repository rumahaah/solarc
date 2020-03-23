from django.db import models

# Create your models here.
class Oppty(models.Model):
	# oppty_id = models.AutoField(primary_key=True)
	oppty_id = models.CharField(max_length=16)
	customer = models.ManyToManyField('Customer')
	project_name = models.CharField(max_length=100)
	def __str__(self):
		# return "%s - %s - %s " % (self.project_name, self.customer.all()[0], self.oppty_id)
		# return "%s & Project %s " % (self.customer.all()[0], self.project_name)
		return "%s & Customer: %s " % (self.project_name, self.customer.all()[0])
	class Meta(object):
		ordering = ['project_name']

class Preproject(models.Model):
	project_status_option = (
		('c', 'Create'),
		('o', 'Open'),
		('b', 'Break'),
	)
	solution_criteria_option = (
		('s', 'Standard'),
		('m', 'Multiservice'),
		('cm', 'Complex MRC > 150JT'),
		('co', 'Complex OTC > 5M'),
		('cn', 'Complex Non Product'),
		('cc', 'Complex Custom Product'),
	)
	progress_option = (
		('w', 'Close Won'),
		('l', 'Close Lost'),
		('p', 'Progress - Internal SA'),
		('s', 'Progress - Submited'),
		('c', 'Cancelled'),
		('h', 'PSA Hold'),
	)
	product_option = (
		('c', 'Connectivity'),
		('i', 'ITS'),
	)
	payment_option = (
		('m', 'MRC'),
		('o', 'OTC'),
	)

	oppty = models.ForeignKey('Oppty', on_delete=models.CASCADE)
	# opportunity_id = models.CharField(max_length=20)
	remark = models.TextField(max_length=1000, blank=True, null=True)
	issues = models.TextField(max_length=1000, blank=True, null=True)
	sa_lintasarta = models.ManyToManyField('Saperson')
	sales_lintasarta = models.ForeignKey('Salesperson', on_delete=models.CASCADE)
	pss_lintasarta = models.ManyToManyField('Pssperson')
	project_status = models.CharField(max_length=1, choices=project_status_option)
	solution_criteria = models.CharField(max_length=2, choices=solution_criteria_option)
	progress = models.CharField(max_length=1, choices=progress_option)
	product = models.CharField(max_length=1, choices=product_option)
	taxsonomi = models.ManyToManyField('Taxsonomi')
	payment = models.CharField(max_length=1, choices=payment_option)
	#timestamp
	table_updated = models.DateField(auto_now=True, auto_now_add=False)
	table_creation_timestamp = models.DateField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return "%s" % (self.oppty)
		# return "%s" % (self.opportunity.all()[0])
		# return "%s & Project %s " % (self.opportunity.all()[0], self.opportunity.all()[0])

# class PSA_PCA(models.Model):
# 	project = models.ForeignKey('Preproject',on_delete=models.CASCADE)
# 	psa_date = models.DateField(auto_now=False, auto_now_add=False)
# 	pca_date = models.DateField(auto_now=False, auto_now_add=False)
# 	remark = models.TextField(max_length=1000)
# 	issues = models.TextField(max_length=1000)
	
# 	#timestamp
# 	table_updated = models.DateField(auto_now=True, auto_now_add=False)
# 	table_creation_timestamp = models.DateField(auto_now=False, auto_now_add=True)
# 	def __str__(self):
# 		return self.psa_date
		

# class Lintasartaperson(models.Model):
# 	initial = models.CharField(max_length=3)
# 	name = models.CharField(max_length=100)
# 	def __str__(self):
# 		return "%s - %s" % (self.initial, self.name)
# 	class Meta:
# 		ordering = ['initial', 'name']

class Saperson(models.Model):
	initial = models.CharField(max_length=3)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	def __str__(self):
		return "%s - %s" % (self.initial, self.name)
	class Meta:
		ordering = ['initial', 'name']

class Pssperson(models.Model):
	initial = models.CharField(max_length=3)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	def __str__(self):
		return "%s - %s" % (self.initial, self.name)
	class Meta:
		ordering = ['initial', 'name']

class Salesperson(models.Model):
	initial = models.CharField(max_length=3)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	def __str__(self):
		return "%s - %s" % (self.initial, self.name)
	class Meta:
		ordering = ['initial', 'name']

class Customer(models.Model):
	segment_option = (
			('0', 'Banking 1'),
			('1', 'Banking 2'),
			('2', 'Finance Non-Bank'),
			('3', 'Supply Chain'),
			('4', 'Public Sector 1'),
			('5', 'Public Sector 2'),
			('6', 'Resources'),
			('7', 'Telco'),
		)
	customer_criteria_option = (
		('0', 'Key Strategic Account'),
		('1', 'Emerging Account'),
		('2', 'Strategic Account'),
		('3', 'New Customer & Not EA'),
		('4', 'Regular'),
	)
	customer_name = models.CharField(max_length=100)
	customer_segment = models.CharField(max_length=1, choices=segment_option)
	customer_criteria = models.CharField(max_length=1, choices=customer_criteria_option)

	def __str__(self):
		if self.customer_criteria == '0':
			customer_criteria_1 = 'KSA'
		elif self.customer_criteria == '1':
			customer_criteria_1 = 'EA'
		elif self.customer_criteria == '2':
			customer_criteria_1 = 'SA'
		elif self.customer_criteria == '3':
			customer_criteria_1 = 'NEW'
		else:
			customer_criteria_1 = 'REG'
		return "%s - %s" % (self.customer_name, customer_criteria_1)
		# return self.customer_name
	class Meta:
		ordering = ['customer_name']

class Taxsonomi(models.Model):
	product_name_option = (
			('0', 'Datacom'),
			('1', 'Cloud'),
			('2', 'Data Center'),
			('3', 'Sec & Col'),
			('4', 'ITO'),
			('5', 'Insol'),
			('6', 'Digital Ads'),
		)
	product_name = models.CharField(max_length=1, choices=product_name_option)

	def __str__(self):
		if self.product_name == '0':
			taxsonomi = 'Datacom'
		elif self.product_name == '1':
			taxsonomi = 'Cloud'
		elif self.product_name == '2':
			taxsonomi = 'Data Center'
		elif self.product_name == '3':
			taxsonomi = 'Sec & Col'
		elif self.product_name == '4':
			taxsonomi = 'ITO'
		elif self.product_name == '5':
			taxsonomi = 'Insol'
		else: 
			taxsonomi = 'Digital Ads'
		return taxsonomi