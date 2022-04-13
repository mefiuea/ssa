from django import forms


from .models import Events


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
