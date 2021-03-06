import pytest
import datetime

from django.test import TestCase, Client
from unittest import skip
from django.urls import reverse
from django import urls
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from management_app.models import Events, Post, Profile, Offers, Comment
from management_app.forms import ProfileEditForm


class TestViews(TestCase):

    def setup(self):
        """Setup client"""
        self.client = Client()

    def create_user_and_login(self):
        """Function to create default user and logging this user in"""
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
        """Test to check status code after GET method and check rendered template"""
        url = reverse('management_app:events_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/events.html')

    def test_event_detailed_view_GET(self):
        """Test to check status code after GET method and check rendered template.
        Test also POST method status code to redirect"""
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
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # profile view require created user profile
        user_profile = Profile.objects.create(owner=user)
        url = reverse('management_app:profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/profile.html')

    @skip
    def test_profile_edit_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # profile view require - created user profile
        user_profile = Profile.objects.create(owner=user)
        url = reverse('management_app:profile_edit_view', args=(user_profile.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/management_app/profile_edit.html')

    def test_profile_edit_view_save_data_POST(self):
        """Test validation form for profile edit"""
        user = self.create_user_and_login()
        # no data need
        form = ProfileEditForm(data={})
        self.assertTrue(form.is_valid())

        # profile view require created user profile
        user_profile = Profile.objects.create(owner=user)
        url = reverse('management_app:profile_edit_view', args=(1,))
        response_post = self.client.post(url, data={'nickname': 'nick'})

    def test_event_add_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        self.create_user_and_login()
        url = reverse('management_app:add_event_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/add_event.html')

    def test_event_add_view_POST(self):
        """Test POST method status code to redirect"""
        self.create_user_and_login()
        url = reverse('management_app:add_event_view')
        response_post = self.client.post(url, data={'title': 'event1', 'place': 'place1',
                                                    'date': datetime.date(2022, 4, 22),
                                                    'time': datetime.time(10, 33, 45)})

        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:profile_view')

    def test_event_edit_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
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
        """Test POST method status code to redirect"""
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
        """Test to check status code after GET method and check if event was created"""
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test2', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_edit_view', args=(event_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Events.objects.all().count(), 1)

    def test_event_delete_view_POST(self):
        """Test POST method for deleting event. First create event and count,
        then delete event by method POST and count"""
        user = self.create_user_and_login()
        # create 1 event to display
        event_1 = Events.objects.create(owner=user, title='title_test', place='place_test',
                                        date=datetime.date(2022, 4, 22), time=datetime.time(10, 33, 45))
        url = reverse('management_app:event_delete_view', args=(event_1.id, ))
        self.assertEqual(Events.objects.all().count(), 1)
        resp_post = self.client.post(url)
        self.assertEqual(Events.objects.all().count(), 0)

    def test_persons_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        self.create_user_and_login()
        url = reverse('management_app:persons_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/persons.html')

    def test_market_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        self.create_user_and_login()
        url = reverse('management_app:market_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/market.html')

    def test_offer_add_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        self.create_user_and_login()
        url = reverse('management_app:add_offer_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/add_offer.html')

    def test_offer_add_view_POST(self):
        """Test POST method status code to redirect and check if validation for 'price' attribute work"""
        self.create_user_and_login()
        url = reverse('management_app:add_offer_view')
        response_post = self.client.post(url, data={'type': 'S', 'title': 'test_title', 'price': 100})
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:profile_view')

        with pytest.raises(ValidationError):
            response_post2 = self.client.post(url, data={'type': 'S', 'title': 'test_title', 'price': 10000})

    def test_offer_detailed_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', price=500)
        url = reverse('management_app:offer_detailed_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/offer_detailed_view.html')

    def test_offer_edit_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', price=500)
        url = reverse('management_app:offer_edit_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/offer_edit_view.html')

    def test_offer_edit_view_POST(self):
        """Test to check edit button. First create one offer, check value for attribute 'type',
        then edit this value and again check if this attribute 'type' has changed to new value"""
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
        """Test to check status code after GET method and count offer"""
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', title='title1', price=500)
        url = reverse('management_app:offer_delete_view', args=(offer_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Offers.objects.all().count(), 1)

    def test_offer_delete_view_POST(self):
        """Test POST method for deleting event. First create event and count,
            then delete event by method POST and count"""
        user = self.create_user_and_login()
        # create 1 offer to display
        offer_1 = Offers.objects.create(owner=user, type='S', title='title1', price=500)
        url = reverse('management_app:offer_delete_view', args=(offer_1.id,))
        self.assertEqual(Offers.objects.all().count(), 1)
        resp_post = self.client.post(url)
        self.assertEqual(Offers.objects.all().count(), 0)

    def test_post_add_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        self.create_user_and_login()
        url = reverse('management_app:add_post_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/add_post.html')

    def test_post_add_view_POST(self):
        """Test POST method status code to redirect and check if validation for 'title' attribute work"""
        user = self.create_user_and_login()
        # create 1 post
        post_1 = Post.objects.create(owner=user, title='test_title', description='desc')
        url = reverse('management_app:add_post_view')
        response_post = self.client.post(url, data={'title': 't' * 200, 'description': 'desc'})
        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('home_page_app:home_view')

        with pytest.raises(ValidationError):
            response_post = self.client.post(url, data={'title': 't' * 201, 'description': 'desc'})

    def test_thread_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # create empty profile for current user
        Profile.objects.create(owner=user)
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='test_title', description='desc')
        url = reverse('management_app:thread_view', args=(post_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/thread.html')

    def test_thread_view_POST(self):
        """Test POST method status code to redirect"""
        user = self.create_user_and_login()
        # create empty profile for current user
        Profile.objects.create(owner=user)
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='test_title', description='desc')
        url = reverse('management_app:thread_view', args=(post_1.id,))

        # add comment button on site. Check if redirect to the same page
        # comments = Comment.objects.all().count()
        # print('KOMENTARZE PRZED = ', comments)
        # response_post = self.client.post(url, data={'owner': user, 'description': 'test_desc'})
        response_post = self.client.post(url)
        # comments = Comment.objects.all().count()
        # print('KOMENTARZE PO = ', comments)

        self.assertEqual(response_post.status_code, 302)
        assert response_post.url == urls.reverse('management_app:thread_view', args=(post_1.id,))

    def test_post_edit_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='title1', description='desc test')
        url = reverse('management_app:post_edit_view', args=(post_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/post_edit_view.html')

    def test_post_edit_view_POST(self):
        """Test to check edit button. First create one post, check value for attribute 'title',
           then edit this value and again check if this attribute 'title' has changed to new value"""
        user = self.create_user_and_login()
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='title1', description='desc test')
        url = reverse('management_app:post_edit_view', args=(post_1.id,))
        # edit data
        # before POST method = save
        self.assertEqual(Post.objects.get(owner=user).title, 'title1')
        resp_post = self.client.post(url, data={'title': 'title edited', 'description': post_1.description})
        self.assertEqual(Post.objects.get(owner=user).title, 'title edited')

    def test_comment_edit_view_GET(self):
        """Test to check status code after GET method and check rendered template"""
        user = self.create_user_and_login()
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='title1', description='desc test')
        # create 1 comment to display
        comment_1 = Comment.objects.create(owner=user, post=post_1, description='desc test')
        url = reverse('management_app:comment_edit_view', args=(post_1.id, comment_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/comment_edit_view.html')

    def test_comment_edit_view_POST(self):
        """Test to check edit button. First create one post and comment, check value for attribute
           'description' for comment, then edit this value and again check if this attribute 'description' has changed
           to new value"""
        user = self.create_user_and_login()
        # create 1 post to display
        post_1 = Post.objects.create(owner=user, title='title1', description='desc test')
        # create 1 comment to display
        comment_1 = Comment.objects.create(owner=user, post=post_1, description='desc test')
        url = reverse('management_app:comment_edit_view', args=(post_1.id, comment_1.id,))
        # edit data
        # before POST method = save
        self.assertEqual(Comment.objects.get(owner=user).description, 'desc test')
        resp_post = self.client.post(url, data={'description': 'desc2'})
        self.assertEqual(Comment.objects.get(owner=user).description, 'desc2')
