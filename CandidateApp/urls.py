from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),

    path('new_application/', save_application, name='save-candidateData'),
    path('applications/', get_application, name='get-candidateData'),
    path('save_profile/', save_profile, name='save_profile'),
    path('get_profile/', get_profile, name='get_profile'),
]