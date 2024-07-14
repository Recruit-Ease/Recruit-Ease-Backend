from django.urls import path
from .views import register_view, logout_view, home_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
]