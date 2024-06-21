from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# models.py
class CompanyManager(BaseUserManager):
    def create_user(self, email, name, address, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, address=address)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, address, password=None):
        user = self.create_user(email, name, address, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Company(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CompanyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Posting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    form_url = models.URLField(null=True)

    def __str__(self):
        return self.title + "-" + self.created_at.strftime('%m-%Y')

class CandidateData(models.Model):
    status_choices = [
        ("Applicaton Submitted", "Application Submitted"),
        ("Under Review", "Under Review"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    resume = models.FileField(upload_to='resumes/', null=True)
    formal_questions = models.JSONField(null=True)
    behavioural_questions = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choices, default='Application Submitted')
    
