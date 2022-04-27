from django.core.exceptions import ValidationError


def picture_size(value):
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('Obrazek zbyt duży. Rozmiar nie powinien przekraczać 1 MB.')
