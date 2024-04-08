# Generated by Django 5.0.3 on 2024-04-06 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_profile_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="First Name"
            ),
        ),
    ]
