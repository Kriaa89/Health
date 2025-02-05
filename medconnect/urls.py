"""
URL configuration for medconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.home, name='home'),  
    path('login/', account_views.user_login, name='login'),
    path('register/', account_views.register, name='register'),
    path('logout/', account_views.user_logout, name='logout'),
    path('doctor-dashboard/', account_views.doctor_dashboard, name='doctor_dashboard'),
    path('nurse-dashboard/', account_views.nurse_dashboard, name='nurse_dashboard'),
    path('patient-dashboard/', account_views.patient_dashboard, name='patient_dashboard'),
    path('doctors/', include('doctors.urls')),
    path('nurses/', include('nurses.urls')),
    path('appointments/', include('appointments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
