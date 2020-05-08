from django.contrib import admin
from .models import  Psa, Pca, Pssho

class PcaAdmin(admin.ModelAdmin):
	pass
	# exclude = ('flagcalc',)

admin.site.register(Psa)
admin.site.register(Pca, PcaAdmin)
admin.site.register(Pssho)