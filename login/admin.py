from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, SuperUser, FAQ

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

