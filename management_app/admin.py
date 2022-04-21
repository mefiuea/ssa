from django.contrib import admin

from . import models

@admin.register(models.Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')


@admin.register(models.Profile)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'nick_name', 'profile_image')


@admin.register(models.Offers)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'offer_image')


@admin.register(models.Post)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'post_image')


@admin.register(models.Comment)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('post', 'owner')
