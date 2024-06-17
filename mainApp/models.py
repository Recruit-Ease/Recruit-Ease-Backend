from django.db import models

class CompanyRegistration(models.Model):
    CompanyID = models.AutoField(primary_key=True)
    CompanyName = models.CharField(max_length=255)
    CompanyEmail = models.EmailField(unique=True)
    CompanyPassword = models.CharField(max_length=128)
    CompanyAddress = models.TextField()

    def __str__(self):
        return self.CompanyName

from django.db import models

class CandidateRegistration(models.Model):
    CandidateID = models.AutoField(primary_key=True)
    CandidateName = models.CharField(max_length=255)
    CandidateEmail = models.EmailField(unique=True)
    CandidatePhone = models.CharField(max_length=15)
    CandidatePassword = models.CharField(max_length=128)

    def __str__(self):
        return self.CandidateName

