# Generated by Django 4.0.4 on 2022-04-13 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Tytuł')),
                ('place', models.CharField(max_length=200, verbose_name='Miejsce')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(verbose_name='Data rozpoczęcia')),
                ('time', models.TimeField(verbose_name='Godzina rozpoczęcia')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
                ('participants_yes', models.PositiveSmallIntegerField(default=0)),
                ('participants_maybe', models.PositiveSmallIntegerField(default=0)),
                ('event_image', models.ImageField(blank=True, default='events_images/default_event_icon.svg', upload_to='events_images', verbose_name='Zdjęcie')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('title2', models.CharField(max_length=200, unique=True, verbose_name='Tytuł')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_date',),
            },
        ),
    ]
