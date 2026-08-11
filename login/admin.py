from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import CustomUser, SuperUser, FAQ, TeamMember, Testimonial, ConsultationBooking

# ==============================================================================
# EXECUTIVE PORTAL BRANDING & HEADERS (KP RegTech & VintushTech)
# ==============================================================================
admin.site.site_header = "Executive Wealth Admin Suite • KP RegTech & VintushTech"
admin.site.site_title = "Executive Wealth Admin Portal"
admin.site.index_title = "Commercial Wealth & Client Operations Dashboard"


@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    """
    Comprehensive Executive Admin Panel for Private Wealth Consultation Bookings.
    Provides complete visibility, filtering, search, status management, and audit tracking.
    """
    list_display = (
        'reference_key', 'client_name', 'service', 'duration_minutes',
        'consultation_date', 'consultation_time', 'colored_status', 'colored_payment', 'created_at'
    )
    list_editable = ()
    list_filter = (
        'status', 'payment_status', 'service', 'duration_minutes',
        'consultation_date', 'preferred_comm', 'created_at'
    )
    search_fields = ('reference_key', 'client_name', 'email', 'phone', 'subject', 'message')
    date_hierarchy = 'consultation_date'
    ordering = ('-consultation_date', '-consultation_time', '-created_at')
    readonly_fields = ('reference_key', 'end_time', 'ip_address', 'created_at', 'updated_at')

    @admin.display(description=_("Status"), ordering="status")
    def colored_status(self, obj):
        css_class = f"status-pill status-pill-{obj.status}"
        return format_html('<span class="{}">{}</span>', css_class, obj.get_status_display())

    @admin.display(description=_("Payment"), ordering="payment_status")
    def colored_payment(self, obj):
        css_class = f"status-pill status-pill-{obj.payment_status}"
        return format_html('<span class="{}">{}</span>', css_class, obj.get_payment_status_display())
    
    fieldsets = (
        (_('Booking Identification & Client'), {
            'fields': (
                'reference_key', 'client_name', 'email', 'phone', 'ip_address'
            )
        }),
        (_('Consultation Schedule & Mode'), {
            'fields': (
                'service', 'duration_minutes', 'consultation_date',
                'consultation_time', 'end_time', 'preferred_comm'
            )
        }),
        (_('Status & Fiduciary Review'), {
            'fields': (
                'status', 'payment_status', 'admin_notes'
            )
        }),
        (_('Rescheduling Audit History'), {
            'classes': ('collapse',),
            'fields': (
                'previous_date', 'previous_time', 'rescheduled_reason'
            )
        }),
        (_('Client Requirements & Scope'), {
            'fields': (
                'subject', 'message'
            )
        }),
        (_('System Timestamps'), {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['action_confirm_booking', 'action_mark_paid', 'action_mark_completed', 'action_cancel_booking']

    @admin.action(description=_("Confirm selected consultation requests"))
    def action_confirm_booking(self, request, queryset):
        count = queryset.update(status='confirmed')
        self.message_user(request, f"{count} consultation booking(s) marked as Confirmed.")

    @admin.action(description=_("Mark payment as received for selected bookings"))
    def action_mark_paid(self, request, queryset):
        count = queryset.update(payment_status='completed', status='paid')
        self.message_user(request, f"{count} booking(s) marked as Paid / Confirmed.")

    @admin.action(description=_("Mark selected consultations as completed"))
    def action_mark_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"{count} consultation(s) marked as Completed.")

    @admin.action(description=_("Cancel selected consultation bookings"))
    def action_cancel_booking(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f"{count} consultation(s) marked as Cancelled.")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin configuration for Testimonial model to manage global client reviews.
    """
    list_display = ('name', 'role', 'location', 'category', 'rating', 'badge_theme', 'card_type', 'is_active', 'order')
    list_editable = ('category', 'badge_theme', 'card_type', 'is_active', 'order')
    list_filter = ('is_active', 'category', 'badge_theme', 'card_type', 'rating')
    search_fields = ('name', 'role', 'location', 'quote')
    ordering = ('order', '-rating')



class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for all CustomUser records.
    Displays custom user fields (bio, avatar_url, auth_provider) and standard fields.
    """
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'auth_provider', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'auth_provider', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    # Extend standard fieldsets to show custom fields
    fieldsets = UserAdmin.fieldsets + (
        (_('Profile Info'), {'fields': ('bio', 'avatar_url', 'auth_provider')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Profile Info'), {
            'classes': ('wide',),
            'fields': ('email', 'bio', 'avatar_url', 'auth_provider'),
        }),
    )

class SuperUserAdmin(CustomUserAdmin):
    """
    Admin configuration specifically for superusers.
    Filters the queryset to only display superusers in the list view.
    """
    model = SuperUser
    
    def get_queryset(self, request):
        # Limit to superusers only
        return super().get_queryset(request).filter(is_superuser=True)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin configuration for FAQ model to perform full CRUD operations.
    Allows managing questions, answers, categories, display order, and publishing status.
    """
    list_display = ('question', 'category', 'order', 'is_active', 'updated_at')
    list_editable = ('order', 'is_active', 'category')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('order', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'category', 'order', 'is_active')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for TeamMember model to perform full CRUD operations.
    Allows managing names, designations, images, order, and publishing status.
    """
    list_display = ('name', 'role', 'order', 'is_active', 'updated_at')
    list_editable = ('role', 'order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'role')
    ordering = ('order', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'image', 'order', 'is_active')
        }),
    )


# Register models in admin panel
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SuperUser, SuperUserAdmin)

# Proactive Debugging: Write a marker file to verify if this file is loaded by the Django process
import os
try:
    with open('admin_loaded.txt', 'w') as f:
        f.write('Loaded successfully')
except Exception:
    pass


