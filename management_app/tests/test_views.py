import pytest

from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django import urls
from django.contrib.auth import get_user_model
import datetime
from django.core.exceptions import ValidationError

from management_app.models import Events, Post, Profile, Offers
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

    def test_event_detailed_view_GET(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        # print('PRINT event detailed view:', event_1.id)
        url = reverse('management_app:event_detailed_view', args=(event_1.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/event_detailed_view.html')

        # post button on site. Check if redirect to the same page
        response_post = self.client.post(url)
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:event_detailed_view', args=(event_1.id, ))

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
                                                    'time': datetime.time(10, 33, 45)})

        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:profile_view')

    def test_event_edit_view_GET(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        # print('PRINT event1:', event_1.id)
        url = reverse('management_app:event_edit_view', args=(event_1.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/event_edit_view.html')

    def test_event_edit_view_POST(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        # print('PRINT event1:', event_1.id)
        url = reverse('management_app:event_edit_view', args=(event_1.id,))
        # edit data
        event_1.title = 'event2'
        event_1.save()
        # print('PRINT', event_1)
        response_post = self.client.post(url, data={'title': event_1.title, 'place': event_1.place,
                                                    'date': event_1.date, 'time': event_1.time})
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:event_detailed_view', args=(event_1.id, ))

    def test_event_delete_view_GET(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test2', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_edit_view', args=(event_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Events.objects.all().count(), 1)

    def test_event_delete_view_POST(self):
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_delete_view', args=(event_1.id, ))
        self.assertEqual(Events.objects.all().count(), 1)
        resp_post = self.client.post(url)
        self.assertEqual(Events.objects.all().count(), 0)

    def test_persons_view_GET(self):
        self.create_user_and_login()
        url = reverse('management_app:persons_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/persons.html')

    def test_market_view_GET(self):
        self.create_user_and_login()
        url = reverse('management_app:market_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/market.html')

    def test_offer_add_view_GET(self):
        self.create_user_and_login()
        url = reverse('management_app:add_offer_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/add_offer.html')

    def test_offer_add_view_POST(self):
        self.create_user_and_login()
        url = reverse('management_app:add_offer_view')
        response_post = self.client.post(url, data={'type': 'S', 'title': 'test_title', 'price': 100})
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:profile_view')

        with pytest.raises(ValidationError):
            response_post2 = self.client.post(url, data={'type': 'S', 'title': 'test_title', 'price': 10000})
            # self.assertEqual(response_post2.status_code, 302)

    def test_offer_detailed_view_GET(self):
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', price=500)
        url = reverse('management_app:offer_detailed_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/offer_detailed_view.html')

    def test_offer_edit_view_GET(self):
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', price=500)
        url = reverse('management_app:offer_edit_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/offer_edit_view.html')

    def test_offer_edit_view_POST(self):
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', title='title1', price=500)
        url = reverse('management_app:offer_edit_view', args=(offer_1.id,))
        # edit data
        offer_1.type = 'Z'
        # before POST method = save
        self.assertEqual(Offers.objects.get(owner=user).type, 'S')
        resp_post = self.client.post(url, data={'type': 'Z', 'title': 'new title', 'price': 100.01})
        self.assertEqual(Offers.objects.get(owner=user).type, 'Z')

    def test_offer_delete_view_GET(self):
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', title='title1', price=500)
        url = reverse('management_app:offer_delete_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Offers.objects.all().count(), 1)

    def test_offer_delete_view_POST(self):
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', title='title1', price=500)
        url = reverse('management_app:offer_delete_view', args=(offer_1.id,))
        self.assertEqual(Offers.objects.all().count(), 1)
        resp_post = self.client.post(url)
        self.assertEqual(Offers.objects.all().count(), 0)
