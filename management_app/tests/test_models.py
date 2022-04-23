import pytest

from django.db import IntegrityError
import datetime

from management_app.models import Events


@pytest.mark.django_db
def test_event_slug_on_creation(fixture_generate_event):
    """Test during creation event slug should equal to title"""
    assert fixture_generate_event.slug == 'title_test-1'


@pytest.mark.django_db
def test_event_unique_title(fixture_create_test_user2, fixture_generate_event):
    """Test to check unique field in model Events for title"""
    with pytest.raises(IntegrityError):
        # create 2 event
        event2 = Events.objects.create(owner=fixture_create_test_user2, title='title_test 1', place='place2',
                                       date=datetime.date(2023, 1, 2), time=datetime.time(11, 20, 11))
