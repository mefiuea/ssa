import pytest

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


'''Test if 1 superuser is created during migrations'''
@pytest.mark.django_db()
def test_creating_superuser_in_migrations():
    current_user_model = get_user_model()
    count = current_user_model.objects.all().count()
    assert count == 1



