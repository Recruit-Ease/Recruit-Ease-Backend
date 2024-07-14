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