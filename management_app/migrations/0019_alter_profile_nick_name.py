# Generated by Django 4.0.4 on 2022-04-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0018_rename_offer_image_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nick_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Ksywa'),
        ),
    ]
