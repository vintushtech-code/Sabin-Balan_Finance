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


class TeamMember(models.Model):
    """
    Model representing a Professional Wealth Advisor/Team Member.
    Allows complete management (create, update, delete) from the Admin Panel.
    """
    name = models.CharField(
        _('Name'),
        max_length=150,
        help_text=_("Full name of the team member.")
    )
    role = models.CharField(
        _('Role/Designation'),
        max_length=150,
        help_text=_("Corporate title or professional role.")
    )
    image = models.ImageField(
        _('Profile Image'),
        upload_to='team/',
        blank=True,
        null=True,
        help_text=_("Upload a high-quality portrait image. If empty, the default placeholder asset will be used.")
    )
    order = models.PositiveIntegerField(
        _('Display Order'),
        default=0,
        help_text=_("Used to order items in the UI. Lower values appear first.")
    )
    is_active = models.BooleanField(
        _('Is Active'),
        default=True,
        help_text=_("Uncheck to temporarily hide this member from the public layout.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Team Member')
        verbose_name_plural = _('Team Members')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """
    Model representing Client Testimonials & Global Reviews.
    Supports interactive galaxy positioning, verification badges, categories, and ratings.
    """
    CATEGORY_CHOICES = (
        ('entrepreneur', 'Entrepreneurs'),
        ('portfolio_manager', 'Portfolio Managers'),
        ('saver', 'Long-term Savers'),
        ('institutional', 'Institutional Investors'),
    )

    name = models.CharField(_('Client Name'), max_length=150)
    role = models.CharField(_('Professional Title / Role'), max_length=150)
    location = models.CharField(_('City / Region'), max_length=100, default='Global')
    quote = models.TextField(_('Testimonial Quote'))
    rating = models.PositiveSmallIntegerField(_('Star Rating (1-5)'), default=5)
    category = models.CharField(_('Category'), max_length=50, choices=CATEGORY_CHOICES, default='entrepreneur')
    avatar_image = models.CharField(_('Avatar Asset Name or URL'), max_length=255, blank=True, default='')
    avatar_file = models.ImageField(_('Uploaded Avatar Photo'), upload_to='testimonials/avatars/', blank=True, null=True)
    is_verified_linkedin = models.BooleanField(_('Verified via LinkedIn'), default=True)
    linkedin_url = models.URLField(_('LinkedIn Profile URL'), blank=True, default='https://linkedin.com')
    pos_x = models.FloatField(_('Map X Position (%)'), default=30.0, help_text=_("X percentage coordinate (0-100) on global map grid"))
    pos_y = models.FloatField(_('Map Y Position (%)'), default=40.0, help_text=_("Y percentage coordinate (0-100) on global map grid"))
    badge_theme = models.CharField(_('Glow Theme'), max_length=30, default='cyan', choices=[
        ('cyan', 'Cyan Glow'),
        ('emerald', 'Emerald Glow'),
        ('amber', 'Amber/Gold Glow'),
        ('violet', 'Violet Glow')
    ])
    card_type = models.CharField(_('Display Card Style'), max_length=30, default='bubble', choices=[
        ('bubble', 'Glowing Organic Bubble'),
        ('glass_card', 'Sleek Dark Glass Card'),
        ('node_only', 'Compact Avatar Node'),
    ])
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['order', '-rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def get_avatar_url(self):
        """Safely retrieves avatar URL from uploaded file, image path string, or empty string."""
        if self.avatar_file:
            try:
                return self.avatar_file.url
            except ValueError:
                pass
        if self.avatar_image:
            return self.avatar_image
        return ''


class ConsultationBooking(models.Model):
    """
    Model representing Private Wealth Management & Financial Advisory Bookings.
    Includes unique 10-character reference key, dynamic scheduling buffers,
    status workflows, and admin rescheduling tracking with before/after comparison.
    """
    SERVICE_CHOICES = (
        ('financial_planning', 'Comprehensive Financial Planning'),
        ('investment', 'Investment & Multi-Asset Portfolio Strategy'),
        ('fixed_deposit', 'Fixed Deposit & High-Yield Preservation'),
        ('wealth_management', 'Private Wealth Management & Family Office'),
        ('retirement', 'Retirement & Legacy Structuring'),
        ('tax_planning', 'Tax Optimization & Fiscal Structuring'),
        ('portfolio_review', 'Institutional Portfolio Diagnostic & Health Check'),
        ('general', 'General Advisory & Wealth Strategy'),
        ('other', 'Bespoke Executive Financial Advisory'),
    )

    DURATION_CHOICES = (
        (30, '30 Minutes — Focused Consultation'),
        (45, '45 Minutes — Strategic Consultation'),
        (60, '60 Minutes — Comprehensive Consultation'),
    )

    COMM_CHOICES = (
        ('video_call', 'Secure Video Conference (Zoom / Google Meet)'),
        ('in_person', 'In-Person Executive Desk (Main Office)'),
        ('phone', 'Direct Private Phone Call'),
        ('email', 'Written Strategic Advisory Briefing'),
    )

    STATUS_CHOICES = (
        ('received', 'Booking Received'),
        ('under_review', 'Pending Confirmation / Under Review'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid / Confirmed'),
        ('payment_pending', 'Payment Pending'),
        ('rescheduled', 'Rescheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('pending', 'Payment Pending'),
        ('completed', 'Payment Received'),
        ('waived', 'Complimentary / Executive Waiver'),
        ('refunded', 'Refunded'),
    )

    reference_key = models.CharField(
        _('Reference Key'),
        max_length=10,
        unique=True,
        db_index=True,
        help_text=_("Unique 10-character alphanumeric tracking key (e.g., GT7K4M9P2X).")
    )
    client_name = models.CharField(_('Client Name'), max_length=150)
    email = models.EmailField(_('Email Address'))
    phone = models.CharField(_('Phone Number'), max_length=30)
    service = models.CharField(_('Consultation Service'), max_length=50, choices=SERVICE_CHOICES, default='financial_planning')
    duration_minutes = models.PositiveIntegerField(_('Duration (Minutes)'), choices=DURATION_CHOICES, default=45)
    consultation_date = models.DateField(_('Consultation Date'))
    consultation_time = models.TimeField(_('Consultation Start Time'))
    end_time = models.TimeField(_('Consultation End Time'), blank=True, null=True)
    
    subject = models.CharField(_('Subject / Purpose'), max_length=255, blank=True, default='')
    message = models.TextField(_('Requirements / Message'), blank=True, default='')
    preferred_comm = models.CharField(
        _('Preferred Communication Method'),
        max_length=30,
        choices=COMM_CHOICES,
        default='video_call'
    )
    
    status = models.CharField(
        _('Booking Status'),
        max_length=30,
        choices=STATUS_CHOICES,
        default='received'
    )
    payment_status = models.CharField(
        _('Payment Status'),
        max_length=30,
        choices=PAYMENT_CHOICES,
        default='pending'
    )
    
    admin_notes = models.TextField(_('Advisor / Admin Internal Notes'), blank=True, default='')
    
    # Rescheduling Audit Log Fields
    previous_date = models.DateField(_('Previous Consultation Date'), null=True, blank=True)
    previous_time = models.TimeField(_('Previous Consultation Time'), null=True, blank=True)
    rescheduled_reason = models.TextField(_('Rescheduling Reason / Note'), blank=True, default='')

    ip_address = models.GenericIPAddressField(_('Client IP Address'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Consultation Booking')
        verbose_name_plural = _('Consultation Bookings')
        ordering = ['-consultation_date', '-consultation_time', '-created_at']

    def __str__(self):
        return f"[{self.reference_key}] {self.client_name} — {self.get_service_display()} ({self.consultation_date} at {self.consultation_time.strftime('%I:%M %p')})"

    @staticmethod
    def generate_unique_reference_key():
        """
        Generates a crisp, 10-character alphanumeric booking reference key
        (e.g., GT7K4M9P2X) excluding ambiguous letters/numbers (0, O, 1, I, L).
        """
        import secrets
        alphabet = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
        while True:
            key = "".join(secrets.choice(alphabet) for _ in range(10))
            if not ConsultationBooking.objects.filter(reference_key=key).exists():
                return key

    def save(self, *args, **kwargs):
        import datetime
        if not self.reference_key:
            self.reference_key = ConsultationBooking.generate_unique_reference_key()

        # Automatically calculate end_time based on consultation_time + duration_minutes
        if self.consultation_time and self.duration_minutes:
            base_datetime = datetime.datetime.combine(datetime.date.today(), self.consultation_time)
            end_datetime = base_datetime + datetime.timedelta(minutes=self.duration_minutes)
            self.end_time = end_datetime.time()

        # Rescheduling detection when updated via admin
        if self.pk:
            orig = ConsultationBooking.objects.filter(pk=self.pk).first()
            if orig:
                date_changed = orig.consultation_date != self.consultation_date
                time_changed = orig.consultation_time != self.consultation_time
                if date_changed or time_changed:
                    self.previous_date = orig.consultation_date
                    self.previous_time = orig.consultation_time
                    if self.status not in ['cancelled', 'completed']:
                        self.status = 'rescheduled'

        super().save(*args, **kwargs)

    @property
    def duration_label(self):
        labels = {
            30: '30 Minutes (Focused Consultation)',
            45: '45 Minutes (Strategic Consultation)',
            60: '60 Minutes (Comprehensive Consultation)',
        }
        return labels.get(self.duration_minutes, f'{self.duration_minutes} Minutes')

    @property
    def status_badge_class(self):
        mapping = {
            'received': 'badge-info',
            'under_review': 'badge-warning',
            'confirmed': 'badge-success',
            'paid': 'badge-gold',
            'payment_pending': 'badge-warning',
            'rescheduled': 'badge-orange',
            'completed': 'badge-primary',
            'cancelled': 'badge-danger',
        }
        return mapping.get(self.status, 'badge-secondary')


class MediaMention(models.Model):
    """
    Model for 'As featured in' media logos (Trust Signals).
    """
    name = models.CharField(_('Publication Name'), max_length=150)
    logo = models.ImageField(_('Logo Image'), upload_to='trust_signals/media_mentions/', blank=True, null=True)
    link = models.URLField(_('Article Link'), blank=True, default='')
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Media Mention')
        verbose_name_plural = _('Media Mentions')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name


class PartnerIntegration(models.Model):
    """
    Model for banking/institutional partners (Trust Signals).
    """
    name = models.CharField(_('Partner Name'), max_length=150)
    logo = models.ImageField(_('Partner Logo'), upload_to='trust_signals/partners/', blank=True, null=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Partner Integration')
        verbose_name_plural = _('Partner Integrations')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name
