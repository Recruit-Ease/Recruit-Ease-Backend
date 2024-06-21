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
    path('postings/', get_postings, name='get-postings'),
    path('delete_posting/', delete_posting, name='delete-posting'),
    path('update_posting/', update_posting, name='update-posting'),

    # Get a Posting Details to Create Form
    path('apply/<str:id>/', get_posting_details, name='get-posting-details'),

    # CRUD operations for PostingForm
    path('save_candidateData/', save_candidateData, name='save-candidateData'),
    path('candidate_data/', get_candidateData, name='get-candidateData'),
]
