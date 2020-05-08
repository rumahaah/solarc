from django.db import models
from preproject.models import Preproject
from psatopca.models import Pca

# Create your models here.
class Handover(models.Model):
	problem_category_option = (
		('n-pr','No Problem - Fulfilled'),
		('e-sc','External - Scope Change'),
		('e-rn','External - Renewal Process'),
		('e-po','External - Conduct PSA After PO'),
		('e-pr','External - Custom Product'),
		('i-pc','Internal - PCA Form'),
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
	)
	pca = models.ForeignKey('psatopca.Pca', on_delete=models.CASCADE)
	# oppty = models.ForeignKey('preproject.Preproject', on_delete=models.CASCADE)
	po_date = models.DateField()
	po_known_date = models.DateField()
	submit_doc_projectcharter_date = models.DateField()
	submit_presales_handover_date = models.DateField()
	remark = models.TextField(max_length=1000, blank=True, null=True)
	pmois_status = models.CharField(max_length=1, choices=pmois_status_option, default='1')
	problem_category = models.CharField(max_length=4, choices=problem_category_option, default='n-pr')

	def __str__(self):
		return "%s - %s - %s" %("Handover",(self.pca.psa.preproject.customer.all()[0].customer_name),self.pca.psa.preproject.project_name)
		# return "%s - %s - %s" %("Handover",(self.pca.psa.preproject.oppty.customer.all()[0].customer_name),self.pca.psa.preproject.oppty.project_name)
		# return "%s - %s" % (self.id, self.pca.psa.preproject.id)

class Cleanproject(models.Model):
	oppty = models.ForeignKey('preproject.Preproject', on_delete=models.CASCADE)
