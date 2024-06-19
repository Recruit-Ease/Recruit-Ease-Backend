from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None

def custom_authenticate(email, password):
    auth_backend = EmailAuthBackend()
    user = auth_backend.authenticate(request=None, username=email, password=password)
    if user and user.is_active:
        return user
    return None
