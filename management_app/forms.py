from django import forms
from django.forms import DateInput

from .models import Events, Profile, Offers


# class DateInput(forms.DateInput):
#     input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('title', 'place', 'date', 'time', 'description', 'event_image')
        widgets = {
            # 'date': DateInput(),
            'date': forms.DateInput(format='%Y-%m-%d',
                                    attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'}),
            'time': TimeInput(),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nick_name', 'lead_replica', 'additional_replica', 'side_replica', 'best_place', 'gear', 'profile_image')


class OffersForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ('type', 'title', 'price', 'url', 'description', 'condition', 'offer_image')
        widgets = {
            'price': forms.NumberInput(attrs={'style': 'width: 120px', 'step': '0.01', 'min': '0', 'max': '9999.99'}),
        }
