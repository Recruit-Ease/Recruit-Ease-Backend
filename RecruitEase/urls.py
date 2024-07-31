"""
URL configuration for RecruitEase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import company_login_view, forgot_password_view, reset_password
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', company_login_view, name='login'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('api/', include('RecruiterApp.urls')),
    path('api/candidate/', include('CandidateApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)