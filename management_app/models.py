from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Events(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='event_creator', on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True, verbose_name='Tytuł')
    place = models.CharField(max_length=200, verbose_name='Miejsce')
    created_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(verbose_name='Data rozpoczęcia')
    time = models.TimeField(verbose_name='Godzina rozpoczęcia')
    description = models.TextField(blank=True, verbose_name='Opis')
    participants = models.ManyToManyField(get_user_model(), related_name='event_participants', blank=True)
    event_image = models.ImageField(upload_to='events_images/', blank=True, null=True, verbose_name='Zdjęcie', default='events_images/default_event_icon.svg')
    slug = models.SlugField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_date', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Profile(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    profile_image = models.ImageField(upload_to='profiles_images/', blank=True, null=True, verbose_name='Zdjęcie', default='profiles_images/default_profile_icon.svg')
    nick_name = models.CharField(max_length=20, blank=True, unique=True, verbose_name='Ksywa')
    best_place = models.CharField(max_length=20, blank=True, verbose_name='Ulubione miejsce')
    lead_replica = models.CharField(max_length=50, blank=True, verbose_name='Replika główna')
    additional_replica = models.CharField(max_length=50, blank=True, verbose_name='Replika dodatkowa')
    side_replica = models.CharField(max_length=50, blank=True, verbose_name='Replika boczna')
    gear = models.TextField(blank=True, verbose_name='Wyposażenie')