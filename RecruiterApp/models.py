from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def generate_refresh_token(self):
        import uuid
        self.refresh_token = str(uuid.uuid4())
        self.save()

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
    questions = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choices, default='Application Submitted')

    def __str__(self):
        return self.first_name + " " + self.last_name