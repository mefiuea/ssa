import pytest

from django.test import TestCase, Client
from django.urls import reverse
from django import urls
from django.contrib.auth import get_user_model
import datetime

from management_app.models import Events, Post, Profile


class TestViews(TestCase):

    def setup(self):
        self.client = Client()

    def test_events_views_GET(self):

        url = reverse('management_app:events_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/events.html')

    def test_event_detailed_view_GET(self):
        # create user
        user_model = get_user_model()
        data = {'username': 'user_name', 'password': 'abcdefgh123'}
        test_user = user_model.objects.create_user(**data)
        test_user.set_password(data.get('password'))
        test_user.save()
        # login user because event detailed view is login protected
        self.client.login(**data)
        # create 1 event to display
        event_1 = Events.objects.create(owner=test_user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_detailed_view', args=(1, ))
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/event_detailed_view.html')

        # post button on site. Check if redirect to the same page
        response_post = self.client.post(url)
        print(response_post)
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:event_detailed_view', args=(1, ))
