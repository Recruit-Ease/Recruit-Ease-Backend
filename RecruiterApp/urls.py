from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),

    # CRUD operations for Posting
    path('new_posting/', create_posting, name='create-posting'),
    path('postings/', get_postings, name='get-postings'),
    # path('update_posting/', update_posting, name='update-posting'),
    # path('delete_posting/', delete_posting, name='delete-posting'),
]