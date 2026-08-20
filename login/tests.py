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

    def test_custom_404_page(self):
        """Verify custom 404 page renders properly with 404 template."""
        response = self.client.get('/404/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_custom_500_page(self):
        """Verify custom 500 page renders properly with 500 template."""
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')

    def test_consultation_pages_accessible(self):
        """Verify consultation and book-consultation routes load with 200 OK."""
        for url_path in ['/consultation/', '/book-consultation/']:
            response = self.client.get(url_path)
            self.assertEqual(response.status_code, 200)

    def test_services_with_query_param(self):
        """Verify services page loads with ?service=portfolio-strategy query."""
        response = self.client.get('/services/?service=portfolio-strategy')
        self.assertEqual(response.status_code, 200)

    def test_legal_compliance_pages(self):
        """Verify all legal and compliance documents load with 200 OK."""
        legal_routes = ['login:privacy_policy', 'login:cookie_policy', 'login:terms_conditions', 'login:aml_kyc', 'login:disclaimer']
        for route in legal_routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)

    def test_contact_page_accessible(self):
        """Verify contact form page loads with 200 OK."""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_custom_user_model_attributes(self):
        """Verify custom user model attributes and initials helper."""
        self.assertEqual(self.admin_user.get_initials(), 'EX')
        self.assertTrue(User.objects.filter(email=self.admin_email).exists())

    def test_xss_sanitization(self):
        """Verify XSS payload sanitization on input."""
        malicious_input = "<script>alert('xss')</script>Hello World"
        cleaned = sanitize_input(malicious_input)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("Hello World", cleaned)

    def test_consultation_dynamic_pricing_rules(self):
        """Verify that 30m=₹3000, 45m=₹5000, 60m=₹8000 are correctly assigned."""
        import datetime
        from .models import ConsultationBooking

        # 30 minutes -> ₹3000
        b30 = ConsultationBooking.objects.create(
            client_name="Arjun Mehta",
            email="arjun.mehta@example.com",
            phone="+91 9876543210",
            duration_minutes=30,
            consultation_date=datetime.date.today() + datetime.timedelta(days=2),
            consultation_time=datetime.time(10, 0)
        )
        self.assertEqual(float(b30.fee_amount), 3000.00)
        self.assertEqual(float(b30.net_amount), 3000.00)
        self.assertEqual(b30.payment_status, 'unpaid')
        self.assertTrue(b30.invoice_number.startswith('INV-'))

        # 45 minutes -> ₹5000
        b45 = ConsultationBooking.objects.create(
            client_name="Priya Sharma",
            email="priya.sharma@example.com",
            phone="+91 9876543211",
            duration_minutes=45,
            consultation_date=datetime.date.today() + datetime.timedelta(days=3),
            consultation_time=datetime.time(11, 0)
        )
        self.assertEqual(float(b45.fee_amount), 5000.00)
        self.assertEqual(float(b45.net_amount), 5000.00)

        # 60 minutes -> ₹8000
        b60 = ConsultationBooking.objects.create(
            client_name="Rohan Verma",
            email="rohan.verma@example.com",
            phone="+91 9876543212",
            duration_minutes=60,
            consultation_date=datetime.date.today() + datetime.timedelta(days=4),
            consultation_time=datetime.time(14, 0)
        )
        self.assertEqual(float(b60.fee_amount), 8000.00)
        self.assertEqual(float(b60.net_amount), 8000.00)

    def test_consultation_admin_status_and_waiver(self):
        """Verify that admin status changes and fee waivers dynamically update tracking and receipts."""
        import datetime
        from .models import ConsultationBooking

        booking = ConsultationBooking.objects.create(
            client_name="Kabir Kapoor",
            email="kabir@example.com",
            phone="+91 9876543213",
            duration_minutes=45,
            consultation_date=datetime.date.today() + datetime.timedelta(days=5),
            consultation_time=datetime.time(15, 0),
            payment_status='unpaid',
            status='received'
        )

        # Test initial tracking API response
        track_url = f"{reverse('login:consultation_track_api')}?key={booking.reference_key}"
        res = self.client.get(track_url)
        self.assertEqual(res.status_code, 200)
        data = res.json()['data']
        self.assertEqual(data['fee_amount'], 5000.00)
        self.assertEqual(data['payment_status'], 'Unpaid / Payment Due')

        # Admin updates booking to Paid
        booking.payment_status = 'paid'
        booking.status = 'confirmed'
        booking.save()

        res = self.client.get(track_url)
        data = res.json()['data']
        self.assertEqual(data['payment_status'], 'Paid / Completed')
        self.assertEqual(data['status'], 'confirmed')

        # Admin grants 100% Fee Waiver (Complimentary)
        booking.payment_status = 'waived'
        booking.save()
        self.assertEqual(float(booking.net_amount), 0.00)
        self.assertEqual(float(booking.discount_amount), 5000.00)

        res = self.client.get(track_url)
        data = res.json()['data']
        self.assertEqual(data['payment_status'], 'Complimentary / Fee Waived')
        self.assertEqual(data['net_amount'], 0.00)

    def test_consultation_automated_emails(self):
        """Verify that booking creation and status updates trigger branded HTML emails."""
        from django.core import mail
        import datetime
        from .models import ConsultationBooking

        mail.outbox.clear()

        # 1. Create new booking -> triggers booking email
        b = ConsultationBooking.objects.create(
            client_name="Vikramaditya Roy",
            email="vikram@example.com",
            phone="+91 9876543299",
            duration_minutes=45,
            consultation_date=datetime.date.today() + datetime.timedelta(days=7),
            consultation_time=datetime.time(16, 0),
        )
        self.assertTrue(len(mail.outbox) >= 1)
        booking_email = mail.outbox[0]
        self.assertIn(b.reference_key, booking_email.subject)
        self.assertIn("vikram@example.com", booking_email.to)
        self.assertIn("Sabin Balan Finance", booking_email.body)

        mail.outbox.clear()

        # 2. Update status to Confirmed -> triggers status update email
        b.status = 'confirmed'
        b.payment_status = 'paid'
        b.meeting_link = 'https://meet.sabinbalanfinance.com/room/GT7K4M'
        b.save()

        self.assertTrue(len(mail.outbox) >= 1)
        update_email = mail.outbox[0]
        self.assertIn(b.reference_key, update_email.subject)
        self.assertIn("Confirmed", update_email.subject)
        self.assertIn("vikram@example.com", update_email.to)

    def test_contact_form_email_notifications(self):
        """Verify that contact form submission triggers confirmation to user and alert to admin."""
        import time
        from django.core import mail
        from django.core.signing import Signer

        mail.outbox.clear()
        signer = Signer()
        past_time = str(int(time.time()) - 5)
        signed_ts = signer.sign(past_time)

        payload = {
            'name': 'Devendra Mehta',
            'email': 'devendra.mehta@example.com',
            'subject': 'Family Office Advisory Inquiry',
            'message': 'We are inquiring regarding multi-jurisdiction fiduciary portfolio restructuring.',
            'website': '',
            'submission_security': signed_ts,
        }
        res = self.client.post(reverse('contactform:contact'), payload, follow=True)
        self.assertEqual(res.status_code, 200)

        # Should send 2 emails: 1 to client, 1 to admin
        self.assertEqual(len(mail.outbox), 2)
        recipients = [m.to[0] for m in mail.outbox]
        self.assertIn('devendra.mehta@example.com', recipients)
        self.assertIn('admin@sabinbalanfinance.com', recipients)

    def test_testimonial_email_notification(self):
        """Verify that submitting a client review alerts the admin desk."""
        from django.core import mail

        mail.outbox.clear()
        payload = {
            'name': 'Aarav Singhania',
            'role': 'Chief Investment Officer',
            'location': 'Mumbai & Singapore',
            'rating': 5,
            'category': 'entrepreneur',
            'quote': 'Sabin Balan Finance engineered unparalleled downside protection for our treasury balance sheet.',
        }
        res = self.client.post(reverse('login:testimonials'), payload, follow=True)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        alert_email = mail.outbox[0]
        self.assertIn('Aarav Singhania', alert_email.subject)
        self.assertIn('admin@sabinbalanfinance.com', alert_email.to)

    def test_admin_2fa_otp_email(self):
        """Verify that 2FA OTP emails are generated with luxury branding strictly for admin login."""
        from django.core import mail
        from django.test import RequestFactory
        from .two_factor import send_2fa_otp

        mail.outbox.clear()
        factory = RequestFactory()
        request = factory.get('/login/')
        # Create session store
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        send_2fa_otp(self.admin_user, request)
        self.assertEqual(len(mail.outbox), 1)
        otp_email = mail.outbox[0]
        self.assertIn(self.admin_email, otp_email.to)
        self.assertIn("Admin 2-Way Verification", otp_email.subject)

    def test_all_models_crud(self):
        """Verify CRUD operations across all system models."""
        from .models import FAQ, TeamMember, Testimonial, MediaMention, PartnerIntegration
        from navfooter.models import SocialMediaLink, NavbarSettings
        from contactform.models import ContactSubmission

        # 1. FAQ Model
        faq = FAQ.objects.create(question="What is FD?", answer="Fixed Deposit advisory.", category="wealth", order=1)
        self.assertEqual(str(faq), "What is FD?")
        self.assertTrue(FAQ.objects.filter(id=faq.id).exists())

        # 2. TeamMember Model
        tm = TeamMember.objects.create(name="Sabin Balan", role="Chief Wealth Strategist", order=1)
        self.assertEqual(str(tm), "Sabin Balan")

        # 3. Testimonial Model
        t = Testimonial.objects.create(name="John Doe", role="Director", quote="Outstanding service", rating=5)
        self.assertEqual(str(t), "John Doe (Director)")

        # 4. MediaMention & PartnerIntegration
        mm = MediaMention.objects.create(name="Bloomberg Finance")
        self.assertEqual(str(mm), "Bloomberg Finance")
        pi = PartnerIntegration.objects.create(name="HDFC Institutional")
        self.assertEqual(str(pi), "HDFC Institutional")

        # 5. SocialMediaLink & NavbarSettings
        SocialMediaLink.objects.filter(platform="whatsapp").delete()
        sml = SocialMediaLink.objects.create(platform="whatsapp", url="https://wa.me/1234567890", is_active=True)
        self.assertIn("WhatsApp", str(sml))
        NavbarSettings.objects.all().delete()
        ns = NavbarSettings.objects.create(logo_image_url="https://example.com/logo.png")
        self.assertEqual(str(ns), "Navbar Configuration Settings")

        # 6. ContactSubmission
        cs = ContactSubmission.objects.create(name="Jane", email="jane@example.com", subject="Audit", message="Hello")
        self.assertIn("Jane", str(cs))



