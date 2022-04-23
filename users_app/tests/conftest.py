import pytest

from django.contrib.auth import get_user_model
from config import settings


@pytest.fixture(scope='session')
def django_db_setup():
    """Fixture to generate new database for test"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': 'db.example.com',
        'NAME': 'external_db',
    }


@pytest.fixture
def fixture_user_data_for_register():
    """Fixture to generate dictionary with user data to register"""
    print('RUN: fixture_user_data_for_register')
    return {'username': 'user_name', 'email': 'a@a.pl', 'password1': 'abcdefgh123', 'password2': 'abcdefgh123'}


@pytest.fixture
def fixture_user_data_for_login():
    """Fixture to generate dictionary with user data to login"""
    print('RUN: fixture_user_data_for_login')
    return {'username': 'user_name', 'password': 'abcdefgh123'}


@pytest.fixture
def fixture_create_test_user(fixture_user_data_for_login):
    """Fixture to create test user"""
    print('RUN: fixture_create_test_user')
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**fixture_user_data_for_login)
    test_user.set_password(fixture_user_data_for_login.get('password'))
    return test_user


@pytest.fixture
def fixture_authenticated_user(client, fixture_user_data_for_login):
    """Fixture to generate authenticated user (user already login)"""
    print('RUN: fixture_authenticated_user')
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**fixture_user_data_for_login)
    test_user.set_password(fixture_user_data_for_login.get('password'))
    test_user.save()
    client.login(**fixture_user_data_for_login)
    return test_user
