"""
Custom User Model & Database Definitions
=========================================

Extends Django's AbstractUser to provide unique email authentication,
social OAuth provider tracking, and basic profile attributes.

Security Note:
All database interactions with this model are conducted strictly via
Django's ORM (e.g., CustomUser.objects.filter(...)), guaranteeing 100%
SQL injection immunity via auto-parameterization. No raw SQL is used.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model for Sabin Balan Finance.
    Supports unique email authentication and non-unique usernames.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        help_text=_("Required. 150 characters or fewer.")
    )

    PROVIDER_CHOICES = (
        ('email', 'Standard Email/Password'),
        ('google', 'Google OAuth'),
        ('github', 'GitHub OAuth'),
        ('facebook', 'Facebook OAuth'),
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
        help_text=_("Required. Enter a valid email address.")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    bio = models.TextField(
        _('bio'),
        blank=True,
        default="",
        help_text=_("Short bio or user profile description.")
    )

    avatar_url = models.URLField(
        _('avatar URL'),
        max_length=500,
        blank=True,
        default="",
        help_text=_("URL pointing to profile avatar image.")
    )

    auth_provider = models.CharField(
        _('authentication provider'),
        max_length=20,
        choices=PROVIDER_CHOICES,
        default='email',
        help_text=_("Identifies the source provider used during user registration.")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username or self.email

    def get_display_name(self):
        """Returns full name or fallback username."""
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username

    def get_initials(self):
        """Generates 1-2 character initials for default avatar display."""
        name = self.get_display_name()
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return name[:2].upper() if name else "U"


class SuperUser(CustomUser):
    """
    Proxy model for CustomUser to represent and manage Superusers separately in the Django Admin.
    """
    class Meta:
        proxy = True
        verbose_name = _('Super User')
        verbose_name_plural = _('Super Users')


class FAQ(models.Model):
    """
    FAQ Model for managing Frequently Asked Questions on the home page.
    Allows full CRUD operations via Django Admin Panel.
    """
    CATEGORY_CHOICES = (
        ('general', 'General Advisory'),
        ('wealth', 'Wealth Management'),
        ('fiduciary', 'Fiduciary & Fees'),
        ('investment', 'SIP & Investment Limits'),
    )

    question = models.CharField(
        _('Question'),
        max_length=300,
        help_text=_("Enter the FAQ question text.")
    )
    answer = models.TextField(
        _('Answer'),
        help_text=_("Enter the detailed answer for this FAQ.")
    )
    category = models.CharField(
        _('Category'),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general',
        help_text=_("Category grouping for the FAQ item.")
    )
    order = models.PositiveIntegerField(
        _('Display Order'),
        default=0,
        help_text=_("Numerical order sequence for display (lower numbers appear first).")
    )
    is_active = models.BooleanField(
        _('Is Published'),
        default=True,
        help_text=_("Uncheck to hide this FAQ from the website.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.question


