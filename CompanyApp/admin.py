from django.contrib import admin
from .models import Company, Posting, PostingForm
# Register your models here.
admin.site.register(Company)
admin.site.register(Posting)
admin.site.register(PostingForm)