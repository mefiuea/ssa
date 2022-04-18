# Generated by Django 4.0.4 on 2022-04-16 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management_app', '0008_remove_events_title2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tytuł')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('offer_image', models.ImageField(upload_to='offers_images/', verbose_name='Zdjęcie')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Cena')),
                ('url', models.URLField(blank=True, verbose_name='Url')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
                ('condition', models.CharField(choices=[('N', 'Nowy'), ('U', 'Używany')], default='N', max_length=8, verbose_name='Stan')),
                ('type', models.CharField(choices=[('S', 'Sprzedam'), ('K', 'Kupię'), ('Z', 'Zamienię')], default='S', max_length=8, verbose_name='Typ')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]