# Generated by Django 5.2.2 on 2025-06-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0005_alter_profile_verify_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='informate_about_views',
            field=models.BooleanField(default=False),
        ),
    ]
