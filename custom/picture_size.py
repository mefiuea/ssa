from django.core.exceptions import ValidationError


def picture_size(value):
    limit = (1024 * 1024) / 2
    if value.size > limit:
        raise ValidationError('Obrazek zbyt duży. Rozmiar nie powinien przekraczać 524 KB.')
