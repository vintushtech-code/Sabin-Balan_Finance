"""
Restructured Portal & Security Test Suite
==========================================

Tests all requirements:
- CustomUser creation and ORM safety
- Honeypot /admin/ returns 404 Not Found
- Secret Admin Portal accessibility via ADMIN_SECRET_PATH
- Public Home, About, Services, and Testimonials routes
- Input sanitization & security defenses
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from login.security import sanitize_input

User = get_user_model()


class SecretAdminAndSecurityTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.secret_slug = getattr(settings, 'ADMIN_SECRET_PATH', 'x7K9mQp2LrT4')
        self.admin_username = "exec_admin"
        self.admin_email = "admin@guardiantreefp.com"
        self.admin_password = "SuperSecretPassword2026!"
        
        self.admin_user = User.objects.create_superuser(
            username=self.admin_username,
            email=self.admin_email,
            password=self.admin_password,
        )

    def test_honeypot_admin_returns_404(self):
        """Verify standard /admin/ returns 404 Not Found camouflage."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 404)

    def test_secret_admin_login_accessible(self):
        """Verify the admin login is accessible under the secret slug."""
        response = self.client.get(f'/{self.secret_slug}/login/')
        self.assertEqual(response.status_code, 200)

    def test_public_pages_accessible_without_auth(self):
        """Verify public web pages (Home, About, Services, Testimonials) are accessible without auth."""
        for url_name in ['login:home', 'login:about', 'login:services', 'login:testimonials']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_custom_user_model_attributes(self):
        """Verify custom user model attributes and initials helper."""
        self.assertEqual(self.admin_user.get_initials(), 'EA')
        self.assertTrue(User.objects.filter(email=self.admin_email).exists())

    def test_xss_sanitization(self):
        """Verify XSS payload sanitization on input."""
        malicious_input = "<script>alert('xss')</script>Hello World"
        cleaned = sanitize_input(malicious_input)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("Hello World", cleaned)

