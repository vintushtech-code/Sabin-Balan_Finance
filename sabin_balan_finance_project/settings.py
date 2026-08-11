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

# Custom User Model & Authentication Redirects
AUTH_USER_MODEL = 'login.CustomUser'
LOGIN_URL = 'login:login'
LOGIN_REDIRECT_URL = 'login:home'
LOGOUT_REDIRECT_URL = 'login:login'

# Email Configuration (Prints password reset & 2FA links/codes to terminal in dev mode)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@guardiantreefp.com')

# --------------------------------------------------------------------------
# 2-Factor Authentication (2FA) & Terminal Verification Settings
# --------------------------------------------------------------------------
# Enforces 6-digit 2FA OTP verification for Admin/Staff user logins.
ADMIN_2FA_ENABLED = os.environ.get('ADMIN_2FA_ENABLED', 'True') == 'True'

# Destination email configuration for 2FA OTP codes:
# - If ADMIN_2FA_EMAIL is empty/unset, codes are sent to the logged-in admin's email address.
# - You can set ADMIN_2FA_EMAIL in environment or here (e.g., 'admin@company.com') to route 2FA emails to a specific inbox.
ADMIN_2FA_EMAIL = os.environ.get('ADMIN_2FA_EMAIL', '')

# Expiration window for 2FA verification codes in seconds (default: 300 seconds = 5 minutes)
ADMIN_2FA_CODE_EXPIRY_SECONDS = int(os.environ.get('ADMIN_2FA_CODE_EXPIRY_SECONDS', '300'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files Configuration for User Uploaded Assets
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

