"""
Login App URL Routing Architecture
===================================

Defines clean, self-contained endpoints for all authentication workflows.
Can be mounted into any Django project's root urls.py with minimal setup.
"""

from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    # Root URL & Main Authenticated Home Page (home.html)
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),

    # Dedicated Private Wealth Consultation & Tracking Routes
    path('consultation/', views.ConsultationView.as_view(), name='consultation'),
    path('book-consultation/', views.ConsultationView.as_view(), name='book_consultation'),
    path('consultation/track/', views.ConsultationView.as_view(), name='consultation_track'),
    path('consultation/api/slots/', views.ConsultationSlotsAPIView.as_view(), name='consultation_slots_api'),
    path('consultation/api/track/', views.ConsultationTrackAPIView.as_view(), name='consultation_track_api'),

    # Core Authentication Routes
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Admin 2-Way Verification (2FA) Routes
    path('verify-2fa/', views.Admin2FAVerifyView.as_view(), name='admin_2fa_verify'),
    path('verify-2fa/resend/', views.Admin2FAResendView.as_view(), name='admin_2fa_resend'),

    # Password Reset Flow Routes
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Social OAuth Routes
    path('oauth/<str:provider>/', views.SocialAuthInitView.as_view(), name='social_init'),
    path('oauth/callback/<str:provider>/', views.SocialAuthCallbackView.as_view(), name='social_callback'),

    # Client First Draft Review & Feedback Portal
    path('client-review/', views.ClientReviewView.as_view(), name='client_review'),
    path('review/', views.ClientReviewView.as_view(), name='review'),
]

