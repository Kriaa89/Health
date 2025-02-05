from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('doctors/', include('doctors.urls')),
    path('nurses/', include('nurses.urls')),
    path('patients/', include('patients.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
