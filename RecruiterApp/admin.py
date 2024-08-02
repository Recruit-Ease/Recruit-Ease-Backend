from django.contrib import admin
from .models import Company, Posting, Application, CompanyProfile

# Register your models here.
admin.site.register(Company)
admin.site.register(Posting)
admin.site.register(Application)
admin.site.register(CompanyProfile)