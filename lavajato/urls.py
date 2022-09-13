from django.contrib import admin
from django.urls import path, include
from . settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plataforma.urls')),
    path('', lambda request: redirect('/home'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
