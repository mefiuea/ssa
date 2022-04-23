import pytest
from config import settings

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime

from management_app.models import Events, Post, Profile

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'HOST': 'db.example.com',
#         'NAME': 'external_db',
#     }


'''Fixture to generate 1 user'''
@pytest.fixture
def fixture_create_test_user2():
    print('RUN: fixture_create_test_user')
    # create user
    user_model = get_user_model()
    data = {'username': 'user_name', 'password': 'abcdefgh123'}
    test_user = user_model.objects.create_user(**data)
    test_user.set_password(data.get('password'))
    test_user.save()

    return test_user


'''Fixture to generate 1 event'''
@pytest.fixture
def fixture_generate_event(fixture_create_test_user2):
    print('RUN: fixture_generate_event')
    event = Events.objects.create(owner=fixture_create_test_user2, title='title_test 1', place='place_test',
                                  date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))

    return event
