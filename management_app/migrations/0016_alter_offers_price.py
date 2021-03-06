# Generated by Django 4.0.4 on 2022-04-18 12:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0015_alter_offers_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Cena PLN'),
        ),
    ]
