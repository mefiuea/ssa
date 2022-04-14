# Generated by Django 4.0.4 on 2022-04-14 11:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='participants_maybe',
        ),
        migrations.RemoveField(
            model_name='events',
            name='participants_yes',
        ),
        migrations.AddField(
            model_name='events',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='event_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]