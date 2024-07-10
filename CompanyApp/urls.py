from django.urls import path
from .views_auth import *
from .views import *

urlpatterns = [
    path('register/', CompanyRegisterView.as_view(), name='company-register'),
    # path('login/', CompanyLoginView.as_view(), name='company-login'),
    path('logout/', CompanyLogoutView.as_view(), name='company-logout'),
    path('get-csrf-token/', GetCSRFToken.as_view(), name='get-csrf-token'),
    path('home/', home, name='home'),
    
    # CRUD operations for Posting
    path('new_posting/', create_posting, name='create-posting'),
]
