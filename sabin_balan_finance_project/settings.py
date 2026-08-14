"""
Django settings for sabin_balan_finance_project project.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import shutil
BASE_DIR = Path(__file__).resolve().parent.parent

# Auto-sync generated image asset if present
_gen_img = r"C:\Users\hp\.gemini\antigravity-ide\brain\1f0cc1a5-b4a9-4802-ae0c-59bc9a6b5caf\financial_advisors_team_1785824626454.png"
_target_img = BASE_DIR / "photos" / "financial_advisors_team.png"
_about_img = BASE_DIR / "photos" / "about_showcase_team.png"
if os.path.exists(_gen_img) and not os.path.exists(_target_img):
    try:
        shutil.copy(_gen_img, _target_img)
    except Exception:
        pass
if os.path.exists(_target_img) and not os.path.exists(_about_img):
    try:
        shutil.copy(_target_img, _about_img)
    except Exception:
        pass
_source_hero = BASE_DIR / "photos" / "hero (2).png"
_about_hero = BASE_DIR / "photos" / "about_us_hero.png"
_gen_about_hero = r"C:\Users\hp\.gemini\antigravity-ide\brain\e5c1b558-8424-4fc8-a645-bca14aa6e8e2\about_hero_1785908291091.png"
_gen_sabin = r"C:\Users\hp\.gemini\antigravity-ide\brain\e5c1b558-8424-4fc8-a645-bca14aa6e8e2\team_sabin_balan_1785916780455.png"
_target_sabin = BASE_DIR / "photos" / "team_sabin.png"
if os.path.exists(_gen_about_hero):
    try:
        shutil.copy(_gen_about_hero, _about_hero)
    except Exception:
        pass
if os.path.exists(_gen_sabin):
    try:
        shutil.copy(_gen_sabin, _target_sabin)
    except Exception:
        pass
elif os.path.exists(_source_hero) and not os.path.exists(_about_hero):
    try:
        shutil.copy(_source_hero, _about_hero)
    except Exception:
        pass

# Testimonials Futuristic UI Image Auto-Sync
_gen_emily = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_emily_carter_1785933234781.png"
_target_emily = BASE_DIR / "photos" / "avatar_emily.png"
_gen_david = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_david_chen_1785933252015.png"
_target_david = BASE_DIR / "photos" / "avatar_david.png"

# Leaders Avatars Auto-Sync
_gen_leader1 = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_leader_1_1785934381986.png"
_target_leader1 = BASE_DIR / "photos" / "avatar_leader1.png"
_gen_leader2 = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_leader_2_1785934401164.png"
_target_leader2 = BASE_DIR / "photos" / "avatar_leader2.png"
_gen_leader3 = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_leader_3_1785934502844.png"
_target_leader3 = BASE_DIR / "photos" / "avatar_leader3.png"
_gen_leader4 = r"C:\Users\hp\.gemini\antigravity-ide\brain\b4ad1d09-66d5-4ecf-8691-671aab032abc\avatar_leader_4_1785934523248.png"
_target_leader4 = BASE_DIR / "photos" / "avatar_leader4.png"

for src, dst in [
    (_gen_emily, _target_emily), 
    (_gen_david, _target_david),
    (_gen_leader1, _target_leader1),
    (_gen_leader2, _target_leader2),
    (_gen_leader3, _target_leader3),
    (_gen_leader4, _target_leader4)
]:
    if os.path.exists(src):
        try:
            shutil.copy(src, dst)
        except Exception:
            pass

_home_hero = BASE_DIR / "photos" / "home_hero.png"
_contact_hero = BASE_DIR / "photos" / "contact_hero.png"
if os.path.exists(_home_hero) and not os.path.exists(_contact_hero):
    try:
        shutil.copy(_home_hero, _contact_hero)
    except Exception:
        pass

# Consultation Hero Image Auto-Sync
_gen_consult_hero = r"C:\Users\hp\.gemini\antigravity-ide\brain\5abf28c0-b259-4695-aba7-e4606bf432bc\consultation_intro_hero_1786171559193.png"
_target_consult_hero = BASE_DIR / "photos" / "consultation_intro.png"
if os.path.exists(_gen_consult_hero):
    try:
        shutil.copy(_gen_consult_hero, _target_consult_hero)
    except Exception:
        pass

# Top About Us Advisory Sections Auto-Sync
_gen_advisory_invaluable = r"C:\Users\hp\.gemini\antigravity-ide\brain\0c81e8e0-392a-44bb-93d5-3e2cb3e15094\about_advisory_invaluable_1786520125025.png"
_target_advisory_invaluable = BASE_DIR / "photos" / "about_advisory_invaluable.png"
if os.path.exists(_gen_advisory_invaluable):
    try:
        shutil.copy(_gen_advisory_invaluable, _target_advisory_invaluable)
    except Exception:
        pass

_gen_best_fit = r"C:\Users\hp\.gemini\antigravity-ide\brain\0c81e8e0-392a-44bb-93d5-3e2cb3e15094\about_best_fit_advisors_1786520222976.png"
_target_best_fit = BASE_DIR / "photos" / "about_best_fit_advisors.png"
if os.path.exists(_gen_best_fit):
    try:
        shutil.copy(_gen_best_fit, _target_best_fit)
    except Exception:
        pass

# Our Mission & Vision Section Auto-Sync
_gen_mv_hero = r"C:\Users\hp\.gemini\antigravity-ide\brain\0c81e8e0-392a-44bb-93d5-3e2cb3e15094\about_mission_vision_hero_1786522626826.png"
_target_mv_hero = BASE_DIR / "photos" / "about_mission_vision_hero.png"
if os.path.exists(_gen_mv_hero):
    try:
        shutil.copy(_gen_mv_hero, _target_mv_hero)
    except Exception:
        pass

_gen_mv_circle = r"C:\Users\hp\.gemini\antigravity-ide\brain\0c81e8e0-392a-44bb-93d5-3e2cb3e15094\about_mission_vision_circle_1786522687112.png"
_target_mv_circle = BASE_DIR / "photos" / "about_mission_vision_circle.png"
if os.path.exists(_gen_mv_circle):
    try:
        shutil.copy(_gen_mv_circle, _target_mv_circle)
    except Exception:
        pass

_gen_mv_board = r"C:\Users\hp\.gemini\antigravity-ide\brain\0c81e8e0-392a-44bb-93d5-3e2cb3e15094\about_mission_vision_board_1786522756897.png"
_target_mv_board = BASE_DIR / "photos" / "about_mission_vision_board.png"
if os.path.exists(_gen_mv_board):
    try:
        shutil.copy(_gen_mv_board, _target_mv_board)
    except Exception:
        pass



# Publisher Logos Auto-Sync (KP RegTech & VintushTech)
_kp_logo_target = BASE_DIR / "photos" / "kplogo.png"
_vintush_logo_target = BASE_DIR / "photos" / "vintushtech_logo.png"

try:
    import urllib.request
    if not os.path.exists(_kp_logo_target):
        req = urllib.request.Request("https://kpregtech.com/static/images/kplogo.png", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response, open(_kp_logo_target, 'wb') as out_file:
            out_file.write(response.read())
except Exception:
    pass

try:
    import urllib.request
    if not os.path.exists(_vintush_logo_target):
        req = urllib.request.Request("https://vintushtech.cloud/static/website/images/favicon.png", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response, open(_vintush_logo_target, 'wb') as out_file:
            out_file.write(response.read())
except Exception:
    pass

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-@wlg*897qb*$lo1_ek^5&5c#bldttck@9$9iah37-)qcf!zd)7')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'contactform',
    'navfooter',
    'theme_config',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sabin_balan_finance_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'theme_config.context_processors.theme_colors',
            ],
        },
    },
]

WSGI_APPLICATION = 'sabin_balan_finance_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'videos',
    BASE_DIR / 'photos',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Secret unguessable slug for Administrator Portal (configurable via env)
ADMIN_SECRET_PATH = os.environ.get('ADMIN_SECRET_PATH', 'x7K9mQp2LrT4').strip('/')

# Custom User Model & Authentication Redirects
AUTH_USER_MODEL = 'login.CustomUser'
LOGIN_URL = f'/{ADMIN_SECRET_PATH}/login/'
LOGIN_REDIRECT_URL = f'/{ADMIN_SECRET_PATH}/'
LOGOUT_REDIRECT_URL = 'login:home'

# ==============================================================================
# EMAIL DISPATCH CONFIGURATION (Terminal / Console Mode)
# ==============================================================================
# In Terminal Mode (Development), all emails (Consultations, Status Updates, 
# Contact Confirmations, Testimonials, and Admin 2FA OTPs) print directly to the 
# terminal console with styled ASCII headers without requiring SMTP servers.
#
# WHEN READY TO SWITCH TO REAL EMAILS:
# 1. Change EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend'
# 2. Configure SMTP credentials (e.g. Gmail App Password, SendGrid, Amazon SES, Mailgun):
#    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
#    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
#    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
#    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_account@gmail.com')
#    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your_app_password')
# ==============================================================================
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Sabin Balan Finance <advisory@sabinbalanfinance.com>')
ADMIN_NOTIFICATION_EMAIL = os.environ.get('ADMIN_NOTIFICATION_EMAIL', 'admin@sabinbalanfinance.com')
CONTACT_FORM_EMAIL_RECIPIENT = ADMIN_NOTIFICATION_EMAIL
SITE_NAME = 'Sabin Balan Finance'
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# --------------------------------------------------------------------------
# 2-Factor Authentication (2FA) & Terminal Verification Settings
# --------------------------------------------------------------------------
# Enforces 6-digit 2FA OTP verification strictly for Admin/Staff user logins.
ADMIN_2FA_ENABLED = os.environ.get('ADMIN_2FA_ENABLED', 'True') == 'True'

# Destination email configuration for 2FA OTP codes:
# - If ADMIN_2FA_EMAIL is empty/unset, codes are sent to the logged-in admin's email address.
# - You can set ADMIN_2FA_EMAIL in environment or here to route 2FA emails to a specific inbox.
ADMIN_2FA_EMAIL = os.environ.get('ADMIN_2FA_EMAIL', '')

# Expiration window for 2FA verification codes in seconds (default: 300 seconds = 5 minutes)
ADMIN_2FA_CODE_EXPIRY_SECONDS = int(os.environ.get('ADMIN_2FA_CODE_EXPIRY_SECONDS', '300'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files Configuration for User Uploaded Assets
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

