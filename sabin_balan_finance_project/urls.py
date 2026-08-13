"""
URL configuration for sabin_balan_finance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from login.views import admin_2fa_login

# Enforce 2-Way Verification (2FA) for Django Admin site authentication
admin.site.login = admin_2fa_login

# Retrieve secret admin slug from settings
ADMIN_SECRET_PATH = getattr(settings, 'ADMIN_SECRET_PATH', 'x7K9mQp2LrT4').strip('/')

# Decoy honeypot handler for standard /admin/ probes
def admin_honeypot_404(request):
    raise Http404("Page not found")

urlpatterns = [
    # Honeypot: Standard /admin/ access returns instant 404 camouflage
    path('admin/', admin_honeypot_404),
    
    # Secret Admin Portal Gateway
    path(f'{ADMIN_SECRET_PATH}/', admin.site.urls),
    
    # Public Client Web Application & Inquiries
    path('contact/', include('contactform.urls')),
    path('', include('login.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Global Custom Error Handlers for 404 Page Not Found and 500 Internal Server Error
handler404 = 'login.views.custom_404_view'
handler500 = 'login.views.custom_500_view'


