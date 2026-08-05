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

# Auto-migrate database modifications on server initialization
try:
    from django.core.management import call_command
    call_command('makemigrations', 'login', interactive=False)
    call_command('migrate', interactive=False)
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
        'DIRS': [],
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

# Email Configuration (Prints password reset links to terminal in dev mode)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@sabinbalanfinance.com')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files Configuration for User Uploaded Assets
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

