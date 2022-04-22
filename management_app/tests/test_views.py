import pytest

from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django import urls
from django.contrib.auth import get_user_model
import datetime

from management_app.models import Events, Post, Profile
from management_app.forms import ProfileEditForm


class TestViews(TestCase):

    def setup(self):
        self.client = Client()

    def create_user_and_login(self):
        # create user
        user_model = get_user_model()
        data = {'username': 'user_name', 'password': 'abcdefgh123'}
        test_user = user_model.objects.create_user(**data)
        test_user.set_password(data.get('password'))
        test_user.save()
        # login user because event detailed view is login protected
        self.client.login(**data)
        return test_user

    def test_events_views_GET(self):
        url = reverse('management_app:events_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/events.html')

    @skip
    def test_event_detailed_view_GET(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_detailed_view', args=(1, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/event_detailed_view.html')

        # post button on site. Check if redirect to the same page
        response_post = self.client.post(url)
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:event_detailed_view', args=(1, ))

    def test_profile_views_GET(self):
        # profile view require created user profile
        user_profile = Profile.objects.create(owner=self.create_user_and_login())
        url = reverse('management_app:profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/profile.html')

    def test_profile_edit_view_GET(self):
        # profile view require created user profile
        user_profile = Profile.objects.create(owner=self.create_user_and_login())
        url = reverse('management_app:profile_edit_view', args=(1, ))
        response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'management_app/management_app/profile_edit.html')

    def test_profile_edit_view_save_data_POST(self):
        user = self.create_user_and_login()
        # no data need
        form = ProfileEditForm(data={})
        self.assertTrue(form.is_valid())

        # profile view require created user profile
        user_profile = Profile.objects.create(owner=user)
        url = reverse('management_app:profile_edit_view', args=(1,))
        response_post = self.client.post(url, data={'nickname': 'nick'})

    def test_event_add_view_GET(self):
        self.create_user_and_login()
        url = reverse('management_app:add_event_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/add_event.html')

    def test_event_add_view_POST(self):
        self.create_user_and_login()
        url = reverse('management_app:add_event_view')
        response_post = self.client.post(url, data={'title': 'event1', 'place': 'place1',
                                                    'date': datetime.date(2022, 4, 22),
                                                    'time':datetime.time(10, 33, 45)})

        print('PRINT response_post:', response_post)
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:profile_view')
