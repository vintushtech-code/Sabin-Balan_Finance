# Generated manually for FAQ model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='Enter the FAQ question text.', max_length=300, verbose_name='Question')),
                ('answer', models.TextField(help_text='Enter the detailed answer for this FAQ.', verbose_name='Answer')),
                ('category', models.CharField(choices=[('general', 'General Advisory'), ('wealth', 'Wealth Management'), ('fiduciary', 'Fiduciary & Fees'), ('investment', 'SIP & Investment Limits')], default='general', help_text='Category grouping for the FAQ item.', max_length=50, verbose_name='Category')),
                ('order', models.PositiveIntegerField(default=0, help_text='Numerical order sequence for display (lower numbers appear first).', verbose_name='Display Order')),
                ('is_active', models.BooleanField(default=True, help_text='Uncheck to hide this FAQ from the website.', verbose_name='Is Published')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
