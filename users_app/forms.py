from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(UserCreationForm):
    """Class to indicate which fields should be displayed in the form in HTML."""
    # email = forms.EmailField(label='Email', widget=forms.TextInput)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
