# Generated by Django 4.0.4 on 2022-04-27 10:08

import custom.picture_size
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0022_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles_images/', validators=[custom.picture_size.picture_size], verbose_name='Zdjęcie'),
        ),
    ]
