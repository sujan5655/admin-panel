# Generated by Django 5.0.6 on 2024-10-29 10:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_book_booking_is_booked_remove_property_seller_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='approval_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='property',
            name='seller',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL),
        ),
    ]
