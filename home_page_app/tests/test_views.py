import pytest

from django.test import TestCase, Client
from django.urls import reverse

from management_app.models import Events, Post, Profile


class TestHomePageViews(TestCase):

    def test_post_events_list_GET(self):
        client = Client()
        print('client: ', client)

        url = reverse('home_page_app:home_view')
        print('url: ', url)

        response = client.get(url)
        print('response: ', response)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page_app/home.html')

