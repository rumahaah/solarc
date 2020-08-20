from django.contrib import admin
from .models import  Handover, Changerequest_overbudget

# Register your models here.
admin.site.register(Handover)
admin.site.register(Changerequest_overbudget)
