from django import forms

from .models import Events, Profile, Offers, Post, Comment


class TimeInput(forms.TimeInput):
    """Overwrite input time to display in form in correct format"""
    input_type = 'time'


class EventsForm(forms.ModelForm):
    """Class to indicate which fields should be displayed in the form in HTML. Additionally,
    widgets that modify specific fields in the form (e.g. how the date, time is displayed)"""
    class Meta:
        model = Events
        fields = ('title', 'place', 'date', 'time', 'description', 'event_image')
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d',
                                    attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'}),
            'time': TimeInput(),
        }


class ProfileEditForm(forms.ModelForm):
    """Class to indicate which fields should be displayed in the form in HTML."""
    class Meta:
        model = Profile
        fields = ('nick_name', 'lead_replica', 'additional_replica', 'side_replica', 'best_place', 'gear', 'profile_image')


class OffersForm(forms.ModelForm):
    """Class to indicate which fields should be displayed in the form in HTML."""
    class Meta:
        model = Offers
        fields = ('type', 'title', 'price', 'url', 'description', 'condition', 'offer_image')
        widgets = {
            'price': forms.NumberInput(attrs={'style': 'width: 120px', 'step': '0.01', 'min': '0', 'max': '9999.99'}),
            'url': forms.URLInput(attrs={'type': ''}),
        }


class PostForm(forms.ModelForm):
    """Class to indicate which fields should be displayed in the form in HTML."""
    class Meta:
        model = Post
        fields = ('title', 'description', 'post_image')


class CommentForm(forms.ModelForm):
    """Class to indicate which fields should be displayed in the form in HTML."""
    class Meta:
        model = Comment
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
