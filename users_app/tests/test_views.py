import pytest

from django.contrib.auth import get_user_model
from django import urls
from django.test import TestCase

from users_app.forms import RegistrationForm


@pytest.mark.django_db()
def test_creating_superuser_in_migrations():
    """Test if 1 superuser is created during migrations"""
    current_user_model = get_user_model()
    count = current_user_model.objects.all().count()
    assert count == 10


@pytest.mark.parametrize('param', (
        ('users_app:signup_view'),
        ('users_app:login_view'),
        ('users_app:logout_view')
))
def test_render_views(client, param):
    """Test if views render urls and return code 200"""
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    # print(resp)
    assert resp.status_code == 200


class SignupFormTest(TestCase):
    """Test signup form validation"""
    def test_signup_user_form_validation(self):
        form = RegistrationForm(data={'username': 'user_name', 'email': 'a@a.pl', 'password1': 'abcdefgh123', 'password2': 'abcdefgh123'})
        self.assertTrue(form.is_valid())


@pytest.mark.django_db
def test_user_signup(client, fixture_user_data_for_register):
    """Test signup for user"""
    user_model = get_user_model()
    assert user_model.objects.count() == 10
    signup_url = urls.reverse('users_app:signup_view')
    resp = client.post(signup_url, fixture_user_data_for_register)
    assert user_model.objects.count() == 11
    assert resp.status_code == 302  # 302 code to redirect after POST method


@pytest.mark.django_db
def test_user_login(client, fixture_create_test_user, fixture_user_data_for_login):
    """Test login for user"""
    user_model = get_user_model()
    assert user_model.objects.count() == 11
    login_url = urls.reverse('users_app:login_view')
    resp = client.post(login_url, data=fixture_user_data_for_login)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home_page_app:home_view')


@pytest.mark.django_db
def test_user_logout(client, fixture_authenticated_user, fixture_user_data_for_login):
    """Test logout for user"""
    # check GET method
    logout_url = urls.reverse('users_app:logout_view')
    resp_get = client.get(logout_url)
    assert resp_get.status_code == 200
    # check POST method
    resp_post = client.post(logout_url)
    assert resp_post.status_code == 200
