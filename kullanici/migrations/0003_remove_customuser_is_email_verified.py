# Generated by Django 5.1.4 on 2024-12-20 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kullanici', '0002_customuser_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_email_verified',
        ),
    ]
