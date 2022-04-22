from django.test import TestCase
from management_app.forms import EventsForm, ProfileEditForm, OffersForm, PostForm, CommentForm
import datetime


class TestForms(TestCase):

    def test_events_form_valid_data(self):
        form = EventsForm(data={
            'title': 'event1',
            'place': 'place1',
            'date': datetime.date(2022, 4, 22),
            'time': datetime.time(10, 33, 45),
            'description': 'desc',
            'event_image': ''
        })

        self.assertTrue(form.is_valid())

    def test_events_form_no_data(self):
        form = EventsForm(data={})

        self.assertFalse(form.is_valid())
        # 4 fields are required
        self.assertEqual(len(form.errors), 4)

    def test_offers_form_valid_data(self):
        form = OffersForm(data={
            'title': 'offer1',
            'price': 100,
            'type': 'S'
        })

        self.assertTrue(form.is_valid())
