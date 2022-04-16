# Generated by Django 4.0.4 on 2022-04-16 21:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0009_offers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999.99)], verbose_name='Cena'),
        ),
    ]
