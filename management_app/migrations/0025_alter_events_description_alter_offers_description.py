# Generated by Django 4.0.4 on 2022-04-27 12:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0024_alter_events_event_image_alter_offers_offer_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(2000)], verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='offers',
            name='description',
            field=models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(1200)], verbose_name='Opis'),
        ),
    ]
