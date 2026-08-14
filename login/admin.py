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
    Provides complete visibility, filtering, search, status management, dynamic billing, and audit tracking.
    """
    list_display = (
        'reference_key', 'client_name', 'service', 'duration_minutes',
        'display_fee', 'payment_status', 'status',
        'consultation_date', 'consultation_time', 'invoice_number'
    )
    list_editable = ('payment_status', 'status')
    list_filter = (
        'status', 'payment_status', 'duration_minutes', 'service',
        'consultation_date', 'preferred_comm', 'created_at'
    )
    search_fields = ('reference_key', 'client_name', 'email', 'phone', 'invoice_number', 'transaction_id', 'subject', 'message')
    date_hierarchy = 'consultation_date'
    ordering = ('-consultation_date', '-consultation_time', '-created_at')
    readonly_fields = ('reference_key', 'end_time', 'net_amount', 'ip_address', 'created_at', 'updated_at')

    @admin.display(description=_("Fee / Net (₹)"), ordering="fee_amount")
    def display_fee(self, obj):
        if not obj.net_amount or obj.payment_status == 'waived':
            return format_html('<span style="color: #059669; font-weight: 700;">₹0 (Waived)</span>')
        try:
            val = float(obj.net_amount)
            return format_html('<strong>₹{:,.0f}</strong> <span style="font-size: 0.8em; color: #64748b;">(Net)</span>', val)
        except Exception:
            return format_html('<strong>₹{}</strong>', obj.net_amount)

    @admin.display(description=_("Status"), ordering="status")
    def colored_status(self, obj):
        color_map = {
            'received': ('#e0f2fe', '#0369a1'),
            'under_review': ('#fef3c7', '#b45309'),
            'confirmed': ('#dcfce7', '#15803d'),
            'paid': ('#fef9c3', '#854d0e'),
            'rescheduled': ('#ffedd5', '#c2410c'),
            'completed': ('#f1f5f9', '#475569'),
            'cancelled': ('#fee2e2', '#b91c1c'),
        }
        bg, fg = color_map.get(obj.status, ('#f1f5f9', '#334155'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; display: inline-block;">{}</span>',
            bg, fg, obj.get_status_display()
        )

    @admin.display(description=_("Payment Status"), ordering="payment_status")
    def colored_payment(self, obj):
        color_map = {
            'paid': ('#dcfce7', '#15803d', 'PAID'),
            'waived': ('#ecfdf5', '#047857', 'WAIVED (FREE)'),
            'unpaid': ('#fee2e2', '#b91c1c', 'UNPAID'),
            'pending': ('#fef3c7', '#b45309', 'PROCESSING'),
            'refunded': ('#f1f5f9', '#64748b', 'REFUNDED'),
        }
        bg, fg, label = color_map.get(obj.payment_status, ('#f1f5f9', '#334155', obj.get_payment_status_display()))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 0.8rem; display: inline-block;">{}</span>',
            bg, fg, label
        )
    
    fieldsets = (
        (_('Booking Identification & Client'), {
            'fields': (
                ('reference_key', 'invoice_number'),
                ('client_name', 'email', 'phone'),
                'ip_address'
            )
        }),
        (_('Consultation Schedule & Mode'), {
            'fields': (
                ('service', 'duration_minutes'),
                ('consultation_date', 'consultation_time', 'end_time'),
                ('preferred_comm', 'fiduciary_desk'),
                'meeting_link'
            )
        }),
        (_('Dynamic Financial Billing & Retainer Management'), {
            'fields': (
                ('fee_amount', 'discount_amount', 'net_amount'),
                ('payment_status', 'payment_method', 'transaction_id')
            )
        }),
        (_('Booking Lifecycle Status & Fiduciary Notes'), {
            'fields': (
                'status',
                'client_instructions',
                'admin_notes'
            )
        }),
        (_('Rescheduling Audit History'), {
            'classes': ('collapse',),
            'fields': (
                ('previous_date', 'previous_time'),
                'rescheduled_reason'
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

    actions = ['action_mark_paid', 'action_mark_unpaid', 'action_mark_waived', 'action_confirm_booking', 'action_mark_completed', 'action_cancel_booking']

    @admin.action(description=_("Mark selected bookings as PAID (Payment Received)"))
    def action_mark_paid(self, request, queryset):
        count = queryset.update(payment_status='paid', status='paid')
        self.message_user(request, f"{count} booking(s) marked as PAID & Confirmed.")

    @admin.action(description=_("Mark selected bookings as UNPAID (Payment Pending)"))
    def action_mark_unpaid(self, request, queryset):
        count = queryset.update(payment_status='unpaid')
        self.message_user(request, f"{count} booking(s) marked as UNPAID.")

    @admin.action(description=_("Grant Full Complimentary Fee Waiver"))
    def action_mark_waived(self, request, queryset):
        for b in queryset:
            b.payment_status = 'waived'
            b.discount_amount = b.fee_amount
            b.net_amount = 0
            b.save()
        self.message_user(request, f"{queryset.count()} booking(s) granted Complimentary Fee Waiver.")

    @admin.action(description=_("Confirm selected consultation requests"))
    def action_confirm_booking(self, request, queryset):
        count = queryset.update(status='confirmed')
        self.message_user(request, f"{count} consultation booking(s) marked as Confirmed & Fiduciary Allocated.")

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


