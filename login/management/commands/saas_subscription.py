"""
Management Command: saas_subscription
======================================
CLI tool to inspect, lock, unlock, renew, or extend SaaS subscription status.
Provided by: VintushTech & KPRegTech for Sabin Balan (GreenTree FD)
"""

from django.core.management.base import BaseCommand
from login.saas_service import (
    get_saas_status,
    unlock_subscription_with_plan,
    get_or_create_saas_subscription,
    SUBSCRIPTION_PLANS
)
import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = "Manage SaaS Subscription state, trial periods, locking, and renewals."

    def add_arguments(self, parser):
        parser.add_argument('--status', action='store_true', help='Display current SaaS subscription details')
        parser.add_argument('--lock', action='store_true', help='Immediately lock the Admin Panel (simulate expiration)')
        parser.add_argument('--unlock', action='store_true', help='Unlock the Admin Panel')
        parser.add_argument('--plan', type=str, choices=list(SUBSCRIPTION_PLANS.keys()), help='Subscription plan code to activate (1_month, 3_months, 6_months, 1_year)')
        parser.add_argument('--extend-trial', type=int, help='Extend trial by specified number of days')
        parser.add_argument('--reset-trial', action='store_true', help='Reset subscription to initial 3-month free trial state')

    def handle(self, *args, **options):
        sub = get_or_create_saas_subscription()

        if options['reset_trial']:
            now = timezone.now()
            sub.is_free_trial = True
            sub.subscription_status = 'active_trial'
            sub.current_plan = 'trial_3_months'
            sub.is_locked = False
            sub.trial_start_date = now
            sub.trial_end_date = now + datetime.timedelta(days=90)
            sub.paid_until = sub.trial_end_date
            sub.notes = '3-Month Free Trial active. Provided by VintushTech & KPRegTech for Sabin Balan (GreenTree FD).'
            sub.save()
            self.stdout.write(self.style.SUCCESS("[RESET] SaaS subscription reset to 3-Month Free Trial (90 days)."))
            return

        if options['lock']:
            sub.is_locked = True
            sub.subscription_status = 'locked_expired'
            sub.save()
            self.stdout.write(self.style.WARNING("[LOCKED] Admin Panel has been locked successfully."))
            return

        if options['unlock']:
            plan = options.get('plan') or '1_year'
            sub, expiry = unlock_subscription_with_plan(plan, simulated_payment=True)
            self.stdout.write(self.style.SUCCESS(f"[UNLOCKED] Admin Panel UNLOCKED! Activated plan: {plan}. Valid until: {expiry}"))
            return

        if options['extend_trial']:
            days = options['extend_trial']
            now = timezone.now()
            sub.is_locked = False
            sub.is_free_trial = True
            sub.subscription_status = 'active_trial'
            sub.trial_end_date = (sub.trial_end_date or now) + datetime.timedelta(days=days)
            sub.paid_until = sub.trial_end_date
            sub.save()
            self.stdout.write(self.style.SUCCESS(f"[EXTENDED] Trial extended by {days} days. New expiry: {sub.trial_end_date}"))
            return

        # Default: Print Status
        status = get_saas_status()
        self.stdout.write(self.style.MIGRATE_HEADING("=================================================="))
        self.stdout.write(self.style.MIGRATE_HEADING("  GreenTree FD -- SaaS Subscription Status"))
        self.stdout.write(self.style.MIGRATE_HEADING("  Provided by: VintushTech & KPRegTech"))
        self.stdout.write(self.style.MIGRATE_HEADING("=================================================="))
        self.stdout.write(f"Client:          {status.get('client_name')}")
        self.stdout.write(f"Status:          {status.get('status_display')}")
        self.stdout.write(f"Is Locked:       {status.get('is_locked')}")
        self.stdout.write(f"Days Remaining:  {status.get('days_remaining')} days")
        self.stdout.write(f"Valid Until:     {status.get('expires_at')}")
        self.stdout.write(f"Current Plan:    {status.get('plan_name')}")
        self.stdout.write(self.style.MIGRATE_HEADING("=================================================="))
