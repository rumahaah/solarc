from django.db import models
from preproject.models import Preproject
from psatopca.models import Pca

# Create your models here.
class Handover(models.Model):
	clean_project_category_option = (
		('n-pr','Clean - Fulfilled'),
		('e-sc','External - Scope Change'),
		('e-rn','External - Renewal Process'),
		('e-po','External - Conduct PSA After PO'),
		('e-pb','External - PO Backdate'),
		('e-pr','External - Custom Product'),
		('i-pc','Internal - PCA Approval'),
		('i-de','Internal - Delay to HO'),
	)
	pmois_status_option = (
		('1','Project Charter - Draft'),
		('2','Project Charter - Waiting Approval Presales GM'),
		('3','Project Charter - Waiting Approval Delivery GM'),
		('4','Project Charter - Waiting Approval PM'),
		('5','Presales Handover - Draft'),
		('6','Presales Handover - Waiting Approval PM'),
		('7','Presales Handover - Approved'),
		('8','Presales Handover - Rejected'),
		('9','Handover Not Required'),
	)
	pca = models.ForeignKey('psatopca.Pca', on_delete=models.CASCADE)
	po_date = models.DateField()
	po_known_date = models.DateField()
	submit_doc_projectcharter_date = models.DateField()
	submit_presales_handover_date = models.DateField()
	remark = models.TextField(max_length=1000, blank=True, null=True)
	pmois_status = models.CharField(max_length=1, choices=pmois_status_option, default='1')
	clean_project_category = models.CharField(max_length=4, choices=clean_project_category_option, default='n-pr')

	def __str__(self):
		return "%s - %s - %s" %("Handover",(self.pca.psa.preproject.customer.all()[0].customer_name),self.pca.psa.preproject.project_name)
		# return "%s - %s - %s" %("Handover",(self.pca.psa.preproject.oppty.customer.all()[0].customer_name),self.pca.psa.preproject.oppty.project_name)
		# return "%s - %s" % (self.id, self.pca.psa.preproject.id)

class Changerequest_overbudget(models.Model):
	overbudget_category_option = (
		('0','Customer CR Only'),
		('1','Overbudget Only - Datacomm Problem On Desk Survey / Coverage'),
		('2','Overbudget Only - Internal SA Problem'),
		('3','Overbudget Only - SoW Problem'),
		('4','Overbudget Only - Delivery Problem'),
		('5','Overbudget Only - Kurs'),
		('6','Customer CR to Overbudget - Increased Revenue - New Proposal Needed'),
		('7','Customer CR to Overbudget - Decreased Revenue'),
		('8','Customer CR to Overbudget - Absorbed Costs'),
	)
	bc_category_options = (
		('s', 'Same as before'),
		('o', 'OpEx'),
		('c', 'CapEx'),
	)
	# tcv_changes_category_options = (
	# )
	# cost_changes_category_options = (
	# )
	pca = models.ForeignKey('psatopca.Pca', on_delete=models.CASCADE)
	overbudget_category = models.CharField(max_length=4, choices=overbudget_category_option)
	remark = models.TextField(max_length=1000, blank=True, null=True)
	bc_category_changes = models.CharField(max_length=4, choices=bc_category_options, default='s')
	ebitda_changes = models.DecimalField(max_digits=10, decimal_places=2)
	irr_changes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	tcv_changes_nominal = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
	# tcv_changes_category = models.CharField(max_length=4, choices=tcv_changes_category_options, default='s')
	# cost_changes_category = models.CharField(max_length=4, choices=cost_changes_category_options, default='s')
	def __str__(self):
		return "%s - %s - %s" %("CR & OB",(self.pca.psa.preproject.customer.all()[0].customer_name),self.pca.psa.preproject.project_name)