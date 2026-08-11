"""
URL configuration for sabin_balan_finance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from login.views import custom_admin_login

# Enforce 2-Way Verification (2FA) for Django Admin site authentication
admin.site.login = custom_admin_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', include('contactform.urls')),
    path('', include('login.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

