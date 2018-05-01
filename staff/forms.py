"""Custom forms for convenience.

Contains convenient intermediary forms for login and similar
applications.
"""

from django import forms
from core import models
from staff.widgets import RichTextWidget
from dal import autocomplete


# Form classes
class LoginForm(forms.Form):
    """A basic login form for staff and administrators."""

    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")


class ContentForm(forms.ModelForm):
    """A generic editor for any kind of content."""

    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'description']
        widgets = {
            'title': forms.widgets.TextInput(),
            'description': RichTextWidget(short=True),
            'authors': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users")
        }
        abstract = True


class StoryForm(ContentForm):
    """The story editor form."""

    class Meta(ContentForm.Meta):
        model = models.Story
        fields = ContentForm.Meta.fields + ['lead', 'text']
        widgets = dict(ContentForm.Meta.widgets, text=RichTextWidget(embed=True), lead=RichTextWidget(short=True))


class ImageForm(ContentForm):
    """Form for image creation."""

    class Meta(ContentForm.Meta):
        model = models.Image
        fields = ContentForm.Meta.fields + ['source']
