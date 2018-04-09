"""Custom forms for convenience.

Contains convenient intermediary forms for login and similar
applications.
"""

from django import forms
from core import models

from dal import autocomplete


# Form classes
class LoginForm(forms.Form):
    """A basic login form for staff and administrators."""

    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")


class ContentForm(forms.ModelForm):
    """A generic editor for any kind of content."""

    authors = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"))

    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'description']


class StoryForm(forms.ModelForm):
    """The story editor form."""

    class Meta:
        model = models.Story
        fields = ['lead', 'text']
        widgets = {'content': forms.HiddenInput()}


class ImageForm(forms.ModelForm):
    """Form for image creation."""

    class Meta:
        model = models.Image
        fields = ['source']
