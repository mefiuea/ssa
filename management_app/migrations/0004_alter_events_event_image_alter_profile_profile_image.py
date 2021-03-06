# Generated by Django 4.0.4 on 2022-04-14 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event_image',
            field=models.ImageField(blank=True, default='events_images/default_event_icon.svg', upload_to='events_images/', verbose_name='Zdjęcie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles_images/default_user_icon.svg', upload_to='images/', verbose_name='Zdjęcie'),
        ),
    ]
