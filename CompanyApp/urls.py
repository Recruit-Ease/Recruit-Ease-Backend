from django.urls import path
from .views import CompanyRegisterView, CompanyLoginView, HomeView, CompanyLogoutView, GetCSRFToken

urlpatterns = [
    path('register/', CompanyRegisterView.as_view(), name='company-register'),
    path('login/', CompanyLoginView.as_view(), name='company-login'),
    path('logout/', CompanyLogoutView.as_view(), name='company-logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('get-csrf-token/', GetCSRFToken.as_view(), name='get-csrf-token'),
]
