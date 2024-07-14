from django.contrib import admin
from .models import Company, Posting, CandidateData

# Register your models here.
admin.site.register(Company)
admin.site.register(Posting)
admin.site.register(CandidateData)