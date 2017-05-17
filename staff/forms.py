"""Custom forms for convenience.

Contains convenient intermediary forms for login and similar
applications.
"""

# Django imports
from django import forms
from core import models


# Form classes
class Login(forms.Form):
    """A basic login form for staff and administrators."""

    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")


class Story(forms.ModelForm):
    class Meta:
        model = models.Story
        fields = ['title', 'authors', 'description', 'lead', 'content']
        widgets = {'content': forms.HiddenInput()}


class Image(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ['title', 'authors', 'description', 'source']