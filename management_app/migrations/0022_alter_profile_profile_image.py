# Generated by Django 4.0.4 on 2022-04-26 19:57

import custom.picture_size
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0021_alter_comment_description_alter_events_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles_images/default_profile_icon.svg', null=True, upload_to='images/', validators=[custom.picture_size.picture_size], verbose_name='Zdjęcie'),
        ),
    ]
