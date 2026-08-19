"""
SaaS Subscription, Access Locking & Automated Backup Test Suite
===============================================================
Provided by: VintushTech & KPRegTech for Sabin Balan (Founder, GreenTree FD)
"""

from django.test import TestCase, Client
from django.conf import settings
from django.utils import timezone
import datetime
from login.saas_service import (
    get_or_create_saas_subscription,
    get_saas_status,
    unlock_subscription_with_plan,
    generate_license_key,
    validate_license_key,
    SUBSCRIPTION_PLANS
)
from login.backup_service import create_live_backup, get_latest_backups_summary
from login.models import AdminSaaSSubscription, AdminBackupLog, CustomUser


class SaaSSubscriptionAndBackupTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_secret = getattr(settings, 'ADMIN_SECRET_PATH', 'x7K9mQp2LrT4').strip('/')
        self.admin_url = f"/{self.admin_secret}/"
        
        self.admin_user = CustomUser.objects.create_superuser(
            username="sabin_admin",
            email="sabin@greentreefd.com",
            password="SecureSabinPassword2026!"
        )

    def test_default_trial_initialization(self):
        """Verify initial 3-month free trial record for Sabin Balan is correctly configured."""
        sub = get_or_create_saas_subscription()
        self.assertTrue(sub.is_free_trial)
        self.assertEqual(sub.subscription_status, 'active_trial')
        self.assertEqual(sub.current_plan, 'trial_3_months')
        self.assertFalse(sub.is_locked)
        self.assertEqual(sub.trial_duration_days, 90)
        self.assertIn("Sabin Balan", sub.client_name)
        self.assertIn("VintushTech", sub.provider_credits)

    def test_saas_status_active_trial(self):
        """Verify get_saas_status reports active trial with positive remaining days."""
        status = get_saas_status()
        self.assertFalse(status['is_locked'])
        self.assertTrue(status['is_free_trial'])
        self.assertGreaterEqual(status['days_remaining'], 89)

    def test_saas_locking_intercepts_admin_access(self):
        """Verify that when the subscription is expired/locked, Admin access returns 403 SaaS lock screen."""
        sub = get_or_create_saas_subscription()
        sub.is_locked = True
        sub.subscription_status = 'locked_expired'
        sub.save()

        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'admin/saas_lock.html')
        self.assertContains(response, "Admin Panel Access Expired", status_code=403)
        self.assertContains(response, "VintushTech", status_code=403)
        self.assertContains(response, "KPRegTech", status_code=403)

    def test_saas_unlock_with_plan(self):
        """Verify activating a subscription plan unlocks the admin panel."""
        sub = get_or_create_saas_subscription()
        sub.is_locked = True
        sub.save()

        # Unlock with 6 months plan
        sub, expiry = unlock_subscription_with_plan('6_months', simulated_payment=True)
        self.assertFalse(sub.is_locked)
        self.assertEqual(sub.subscription_status, 'active_paid')
        self.assertEqual(sub.current_plan, '6_months')
        self.assertFalse(sub.is_free_trial)

        status = get_saas_status()
        self.assertFalse(status['is_locked'])
        self.assertGreater(status['days_remaining'], 170)

    def test_license_key_validation(self):
        """Verify license key generator and validation logic."""
        key = generate_license_key('1_year', 'sabin@greentreefd.com')
        is_valid, plan, msg = validate_license_key(key, 'sabin@greentreefd.com')
        self.assertTrue(is_valid)
        self.assertEqual(plan, '1_year')

        # Master developer key
        is_dev_valid, dev_plan, _ = validate_license_key('VINTUSHTECH-KPREGTECH-MASTER-2026')
        self.assertTrue(is_dev_valid)

        # Invalid key
        is_invalid, _, _ = validate_license_key('INVALID-FAKE-KEY')
        self.assertFalse(is_invalid)

    def test_automated_database_backup_generation(self):
        """Verify live database backup generates snapshot and log entry."""
        res = create_live_backup(event_trigger="Test Suite Execution")
        self.assertTrue(res['success'])
        self.assertTrue(res['file_name'].startswith("greentree_db_backup_"))
        self.assertGreater(res['file_size_kb'], 0)

        # Verify summary
        summary = get_latest_backups_summary()
        self.assertGreaterEqual(summary['total_backups'], 1)
        self.assertEqual(summary['status'], 'HEALTHY & SYNCHRONIZED')
