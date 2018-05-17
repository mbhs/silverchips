"""Custom forms for the public interface."""

from django import forms
from core import models
from staff.widgets import RichTextWidget
from dal import autocomplete
from crispy_forms.helper import FormHelper


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    pass # STUB_COMMENT