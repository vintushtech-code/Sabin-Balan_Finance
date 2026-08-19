"""
Sabin Balan Finance — Centralized Luxury Email & Terminal Dispatch Service.
Handles HTML email rendering, fallback generation, context injection, and console/SMTP routing.

To switch from Terminal (Console) Mode to Real SMTP:
1. Open sabin_balan_finance_project/settings.py
2. Set EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
3. Provide EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS = True
"""

import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


def send_luxury_email(subject, template_name, context, recipient_list, from_email=None, fail_silently=True):
    """
    Renders and sends a premium branded HTML email with automatic plain-text fallback.
    Logs email dispatches cleanly to terminal console.
    """
    if not recipient_list:
        logger.warning("[Email Engine] No recipients specified for email: %s", subject)
        return False

    # Default branding context
    default_context = {
        'site_name': getattr(settings, 'SITE_NAME', 'Sabin Balan Finance'),
        'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
        'contact_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'advisory@sabinbalanfinance.com'),
    }
    merged_context = {**default_context, **context}

    sender = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'advisory@sabinbalanfinance.com')

    try:
        html_message = render_to_string(template_name, merged_context)
        plain_message = strip_tags(html_message).strip()
    except Exception as e:
        logger.error("[Email Engine] Error rendering email template %s: %s", template_name, e)
        plain_message = f"Sabin Balan Finance Notification: {subject}"
        html_message = None

    # Print a clean terminal summary header during development
    recipients_str = ", ".join(recipient_list)
    try:
        print("\n" + "=" * 70)
        print(f"[SABIN BALAN FINANCE EMAIL DISPATCH]")
        print(f"   To:      {recipients_str}")
        print(f"   From:    {sender}")
        print(f"   Subject: {subject}")
        print("=" * 70 + "\n")
    except Exception:
        pass

    try:
        sent_count = send_mail(
            subject=subject,
            message=plain_message,
            from_email=sender,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently
        )
        logger.info("[Email Engine] Dispatched email '%s' to %s (Sent: %s)", subject, recipients_str, sent_count)
        return sent_count > 0
    except Exception as e:
        logger.error("[Email Engine] Failed to dispatch email '%s' to %s: %s", subject, recipients_str, e)
        return False


# ------------------------------------------------------------------------------
# Specialized Domain Email Dispatchers
# ------------------------------------------------------------------------------

def send_consultation_booking_email(booking):
    """
    Sends consultation booking confirmation to client and admin notification.
    """
    subject = f"Consultation Confirmed: #{booking.reference_key} — Sabin Balan Finance"
    context = {
        'booking': booking,
    }
    # 1. Send confirmation to Client
    send_luxury_email(
        subject=subject,
        template_name='emails/consultation_booking_email.html',
        context=context,
        recipient_list=[booking.email]
    )

    # 2. Send notification to Admin Desk
    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'admin@sabinbalanfinance.com')
    if admin_email and admin_email != booking.email:
        admin_subject = f"[New Booking] #{booking.reference_key} — {booking.client_name} ({booking.duration_minutes}m - {booking.fee_amount_display})"
        send_luxury_email(
            subject=admin_subject,
            template_name='emails/consultation_booking_email.html',
            context=context,
            recipient_list=[admin_email]
        )


def send_consultation_status_email(booking, old_status=None, old_payment_status=None, is_rescheduled=False, previous_schedule=None, updated_schedule=None):
    """
    Dispatches dynamic status change and schedule revision notification to client.
    """
    status_label = booking.get_status_display()
    payment_label = booking.get_payment_status_display()
    subject = f"Update on Consultation #{booking.reference_key}: {status_label} ({payment_label})"
    
    context = {
        'booking': booking,
        'old_status': old_status,
        'old_payment_status': old_payment_status,
        'is_rescheduled': is_rescheduled,
        'previous_schedule': previous_schedule,
        'updated_schedule': updated_schedule,
    }
    
    return send_luxury_email(
        subject=subject,
        template_name='emails/consultation_status_update_email.html',
        context=context,
        recipient_list=[booking.email]
    )


def send_contact_form_emails(submission):
    """
    Sends client acknowledgement and admin alert on contact form submissions.
    """
    # 1. Confirmation to Client
    client_subject = f"Inquiry Received: {submission.subject} — Sabin Balan Finance"
    send_luxury_email(
        subject=client_subject,
        template_name='emails/contact_confirmation_email.html',
        context={'submission': submission},
        recipient_list=[submission.email]
    )

    # 2. Alert to Admin
    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', getattr(settings, 'CONTACT_FORM_EMAIL_RECIPIENT', 'admin@sabinbalanfinance.com'))
    admin_subject = f"🚨 New Client Inquiry: {submission.subject} from {submission.name}"
    send_luxury_email(
        subject=admin_subject,
        template_name='emails/contact_admin_alert_email.html',
        context={'submission': submission},
        recipient_list=[admin_email]
    )


def send_testimonial_email(testimonial):
    """
    Sends acknowledgement to user and admin notification on new review submission.
    """
    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'admin@sabinbalanfinance.com')
    subject = f"⭐ New Client Review Submitted by {testimonial.name} ({testimonial.rating} Stars)"
    return send_luxury_email(
        subject=subject,
        template_name='emails/testimonial_received_email.html',
        context={'testimonial': testimonial},
        recipient_list=[admin_email]
    )
