import pytest

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


'''Fixture to generate dictionary with user data to register'''
@pytest.fixture
def fixture_user_data_for_register():
    print('RUN: fixture_user_data_for_register')
    return {'username': 'user_name', 'email': 'a@a.pl', 'password1': 'abcdefgh123', 'password2': 'abcdefgh123'}


'''Fixture to generate dictionary with user data to login'''
@pytest.fixture
def fixture_user_data_for_login():
    print('RUN: fixture_user_data_for_login')
    return {'username': 'user_name', 'password': 'abcdefgh123'}


'''Fixture to create test user'''
@pytest.fixture
def fixture_create_test_user(fixture_user_data_for_login):
    print('RUN: fixture_create_test_user')
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**fixture_user_data_for_login)
    test_user.set_password(fixture_user_data_for_login.get('password'))
    return test_user


'''Fixture to generate authenticated user (user already login)'''
@pytest.fixture
def fixture_authenticated_user(client, fixture_user_data_for_login):
    print('RUN: fixture_authenticated_user')
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**fixture_user_data_for_login)
    test_user.set_password(fixture_user_data_for_login.get('password'))
    test_user.save()
    client.login(**fixture_user_data_for_login)
    return test_user
