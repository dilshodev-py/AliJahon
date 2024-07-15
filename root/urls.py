from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root import settings
from teacher.admin import teacher_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher-admin/', teacher_site.urls),
    path('', include('apps.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
