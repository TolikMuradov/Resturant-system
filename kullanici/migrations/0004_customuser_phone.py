# Generated by Django 5.1.4 on 2024-12-21 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullanici', '0003_remove_customuser_is_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
