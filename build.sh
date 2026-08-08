#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python -c "import os, django; os.environ['DJANGO_SETTINGS_MODULE']='sabin_balan_finance_project.settings'; django.setup(); from django.test import RequestFactory; from django.contrib.auth.models import AnonymousUser; from login.views import TestimonialsView, HomeView, AboutView; rf = RequestFactory(); req = rf.get('/'); req.user = AnonymousUser(); t = TestimonialsView(); t.setup(req); t.get_context_data(); h = HomeView(); h.setup(req); h.get_context_data(); a = AboutView(); a.setup(req); a.get_context_data();"
