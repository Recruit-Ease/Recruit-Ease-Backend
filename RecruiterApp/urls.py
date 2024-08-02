from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),

    # CRUD operations for Posting
    path('new_posting/', create_posting, name='create-posting'),
    path('postings/', get_postings, name='get-postings'),
    path('update_posting/', update_posting, name='update-posting'),
    path('delete_posting/', delete_posting, name='delete-posting'),

    path('applications/', get_application, name='get-applications'),
    path('delete_application/', delete_application, name='delete-application'),

    path('apply/<str:id>/', get_posting_details, name='get-posting-details'),
    path('change_status/', change_status, name='change-status'),
    path('send_email/', send_email_candidate, name='send-email'),
    path('save_profile/', save_profile, name='save_profile'),
    path('get_profile/', get_profile, name='get_profile')
]