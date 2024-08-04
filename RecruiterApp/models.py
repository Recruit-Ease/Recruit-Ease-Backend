from django.db import models
from CandidateApp.models import Candidate
import uuid
from django.contrib.auth.hashers import make_password, check_password

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_refresh_token(self):
        refresh_token = str(uuid.uuid4())
        Tokens.objects.create(email=self, token=refresh_token)
        return refresh_token

class Tokens(models.Model):
    email = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {self.token}"

class CompanyProfile(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    profile_pic = models.TextField(null=True)
    tagline = models.CharField(max_length=255, null=True)
    about_us = models.TextField(null=True)

class Posting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True)
    soft_skills = models.JSONField(null=True)
    technical_skills = models.JSONField(null=True)
    questions = models.JSONField(null=True)
    recruiter_name = models.CharField(max_length=255, null=True)
    recruiter_email = models.EmailField(null=True)
    about_job = models.TextField(null=True)
    about_company = models.TextField(null=True)
    qualification = models.TextField(null=True)
    key_requirements = models.TextField(null=True)
    nice_to_have = models.TextField(null=True)
    other_remarks = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    form_url = models.URLField(null=True)

    def __str__(self):
        return self.title + "-" + self.posting_date.strftime('%m-%Y')

class Application(models.Model):
    status_choices = [
        ("Applicaton Submitted", "Application Submitted"),
        ("Under Review", "Under Review"),
        ("Interview Scheduled", "Interview Scheduled"),
        ("Under Evaluation", "Under Evaluation"),
        ("Offer Sent", "Offer Sent"),
        ("Offer Accepted", "Offer Accepted"),
        ("Offer Declined", "Offer Declined"),
        ("Not Selected", "Not Selected"),
    ]

    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    legal_questions = models.JSONField(null=True)
    questions = models.JSONField(null=True)
    resume = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choices, default='Application Submitted')
    offer = models.TextField(null=True)

    def __str__(self):
        return self.candidate.name + " - " + self.posting.title

