import pytest

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


'''Fixture to create 1 user from django.contrib.auth.models'''
@pytest.fixture()
@pytest.mark.django_db()
def fixture_user_instance():
    current_user_model = get_user_model()
    user_instance = current_user_model.objects.create_user('name', 'test@test.pl', 'password')
    return user_instance
