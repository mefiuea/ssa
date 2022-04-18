# Generated by Django 4.0.4 on 2022-04-17 18:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0013_alter_offers_offer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999.99)], verbose_name='Cena PLN'),
        ),
    ]