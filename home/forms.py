"""Custom forms for the public interface."""

from django import forms
from core import models
from staff.widgets import RichTextWidget
from dal import autocomplete
from crispy_forms.helper import FormHelper


class ContentForm(forms.ModelForm):
    """A generic editor for any kind of content."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'guest_authors', 'description']
        widgets = {
            'title': forms.widgets.TextInput(),
            'description': RichTextWidget(short=True),
            'authors': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users")
        }
        abstract = True
