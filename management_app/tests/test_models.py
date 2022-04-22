import pytest

from django.test import TestCase, Client
from django.urls import reverse
from django import urls
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import datetime

from management_app.models import Events, Post, Profile


'''Test during creation event slug should equal to title'''
@pytest.mark.django_db
def test_event_slug_on_creation(fixture_generate_event):
    assert fixture_generate_event.slug == 'title_test-1'


'''Test to check unique field in model Events for title'''
@pytest.mark.django_db
def test_event_unique_title(fixture_create_test_user2, fixture_generate_event):
    with pytest.raises(IntegrityError):
        # create 2 event
        event2 = Events.objects.create(owner=fixture_create_test_user2, title='title_test 1', place='place2',
                                       date=datetime.date(2023, 1, 2), time=datetime.time(11, 20, 11))

