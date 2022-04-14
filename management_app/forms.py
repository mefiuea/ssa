from django import forms

from .models import Events, Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('title', 'place', 'date', 'time', 'description', 'event_image', 'slug')
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nick_name', 'lead_replica', 'additional_replica', 'side_replica', 'best_place', 'gear', 'profile_image')
