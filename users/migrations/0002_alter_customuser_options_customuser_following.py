# Generated by Django 5.0.6 on 2024-05-18 21:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={},
        ),
        migrations.AddField(
            model_name="customuser",
            name="following",
            field=models.ManyToManyField(
                related_name="followers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
