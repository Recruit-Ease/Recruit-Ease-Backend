from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import uuid

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_refresh_token(self):
        self.refresh_token = str(uuid.uuid4())
        self.save()

class CandidateProfile(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=255)
    address = models.TextField()
    short_bio = models.TextField()

    def __str__(self):
        return self.candidate.name