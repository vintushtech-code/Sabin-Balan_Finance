# Generated for Sabin Balan Finance - Consultation Dynamic Pricing & Billing Fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_mediamention_partnerintegration'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationbooking',
            name='fee_amount',
            field=models.DecimalField(decimal_places=2, default=5000.0, help_text='Standard advisory fee in INR (₹3,000 for 30m, ₹5,000 for 45m, ₹8,000 for 60m).', max_digits=10, verbose_name='Consultation Fee (₹)'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Fee reduction or institutional promotional credit in INR.', max_digits=10, verbose_name='Discount / Waiver (₹)'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='net_amount',
            field=models.DecimalField(decimal_places=2, default=5000.0, help_text='Final net amount due or paid.', max_digits=10, verbose_name='Net Amount Due (₹)'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='invoice_number',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Invoice / Tax Ref Number'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='payment_method',
            field=models.CharField(blank=True, default='UPI / Net Banking / Card', max_length=50, verbose_name='Payment Mode'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Transaction ID / UTR Ref'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='fiduciary_desk',
            field=models.CharField(blank=True, default='Senior Wealth Advisory & Fiduciary Desk', max_length=150, verbose_name='Assigned Fiduciary / Desk'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='meeting_link',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Encrypted Meeting URL / Room Link'),
        ),
        migrations.AddField(
            model_name='consultationbooking',
            name='client_instructions',
            field=models.TextField(blank=True, default='1. Secure encrypted meeting link will be dispatched 30 mins prior to schedule.\n2. Please have recent asset allocation summaries or tax returns ready.\n3. 24-hour advance notice requested for calendar adjustments.', verbose_name='Pre-Session Preparation Checklist'),
        ),
        migrations.AlterField(
            model_name='consultationbooking',
            name='duration_minutes',
            field=models.PositiveIntegerField(choices=[(30, '30 Minutes — Focused Consultation (₹3,000)'), (45, '45 Minutes — Strategic Consultation (₹5,000)'), (60, '60 Minutes — Comprehensive Consultation (₹8,000)')], default=45, verbose_name='Duration (Minutes)'),
        ),
        migrations.AlterField(
            model_name='consultationbooking',
            name='payment_status',
            field=models.CharField(choices=[('unpaid', 'Unpaid / Payment Due'), ('paid', 'Paid / Completed'), ('waived', 'Complimentary / 100% Retainer Waived'), ('pending', 'Payment Processing / Pending Verification'), ('refunded', 'Refunded')], default='unpaid', max_length=30, verbose_name='Payment Status'),
        ),
        migrations.AlterField(
            model_name='consultationbooking',
            name='status',
            field=models.CharField(choices=[('received', 'Booking Received'), ('under_review', 'Pending Confirmation / Under Review'), ('confirmed', 'Confirmed & Fiduciary Allocated'), ('paid', 'Paid & Confirmed'), ('rescheduled', 'Rescheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='received', max_length=30, verbose_name='Booking Status'),
        ),
    ]
