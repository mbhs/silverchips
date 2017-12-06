"""Custom forms for convenience.

Contains convenient intermediary forms for login and similar
applications.
"""

from django import forms
from core import models

from dal import autocomplete


# Form classes
class Login(forms.Form):
    """A basic login form for staff and administrators."""

    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")

class Story(forms.ModelForm):
    """The story editor form."""

    authors = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"))

    class Meta:
        model = models.Story
        fields = ['title', 'description', 'lead', 'text']
        widgets = {'content': forms.HiddenInput()}


class Image(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ['title', 'authors', 'description', 'source']
