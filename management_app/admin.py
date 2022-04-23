from django.contrib import admin

from . import models


@admin.register(models.Events)
class EventsAdmin(admin.ModelAdmin):
    """Class to add Events model with displays attributes in django admin panel.
    This allows to modify data in database from django admin panel."""
    list_display = ('title', 'owner')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Class to add Profile model with displays attributes in django admin panel.
    This allows to modify data in database from django admin panel."""
    list_display = ('owner', 'nick_name', 'profile_image')


@admin.register(models.Offers)
class OffersAdmin(admin.ModelAdmin):
    """Class to add Offers model with displays attributes in django admin panel.
    This allows to modify data in database from django admin panel."""
    list_display = ('title', 'owner', 'offer_image')


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Class to add Post model with displays attributes in django admin panel.
    This allows to modify data in database from django admin panel."""
    list_display = ('title', 'owner', 'post_image')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Class to add Comment model with displays attributes in django admin panel.
    This allows to modify data in database from django admin panel."""
    list_display = ('post', 'owner')
