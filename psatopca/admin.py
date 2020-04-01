from django.contrib import admin
from .models import  Psa, Pca

class PcaAdmin(admin.ModelAdmin):
    pass
    # exclude = ('flagcalc',)

admin.site.register(Psa)
admin.site.register(Pca, PcaAdmin)