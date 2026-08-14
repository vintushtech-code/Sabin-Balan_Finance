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
    # Root URL & Main Public Home Page (home.html)
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),

    # Dedicated Private Wealth Consultation & Tracking Routes
    path('consultation/', views.ConsultationView.as_view(), name='consultation'),
    path('book-consultation/', views.ConsultationView.as_view(), name='book_consultation'),
    path('consultation/track/', views.ConsultationView.as_view(), name='consultation_track'),
    path('consultation/api/slots/', views.ConsultationSlotsAPIView.as_view(), name='consultation_slots'),
    path('consultation/api/slots/v1/', views.ConsultationSlotsAPIView.as_view(), name='consultation_slots_api'),
    path('consultation/api/track/', views.ConsultationTrackAPIView.as_view(), name='consultation_track_api'),

    # Client Authentication Suite
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('auth/<str:provider>/', views.SocialAuthInitView.as_view(), name='social_init'),
    path('auth/<str:provider>/callback/', views.SocialAuthCallbackView.as_view(), name='social_callback'),

    # Administrator 2-Way Verification (2FA) Routes
    path('verify-2fa/', views.Admin2FAVerifyView.as_view(), name='admin_2fa_verify'),
    path('verify-2fa/resend/', views.Admin2FAResendView.as_view(), name='admin_2fa_resend'),

    # Staff / Admin Session Termination
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Direct Preview Routes for Custom Error Pages (404 & 500)
    path('404/', views.custom_404_view, name='error_404'),
    path('500/', views.custom_500_view, name='error_500'),

    # Institutional Documentation & Legal Compliance Suite
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('cookie-policy/', views.CookiePolicyView.as_view(), name='cookie_policy'),
    path('terms-and-conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('aml-kyc/', views.AMLKYCView.as_view(), name='aml_kyc'),
    path('disclaimer/', views.DisclaimerView.as_view(), name='disclaimer'),

]


