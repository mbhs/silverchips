"""Custom forms for the public interface."""

from django import forms
from core import models
from staff.widgets import RichTextWidget
from dal import autocomplete
from crispy_forms.helper import FormHelper


class TagSearchForm(forms.Form):
    """Form for searching through tags."""
    name = forms.CharField(label="Name:", required=True, max_length=32)
    helper = FormHelper()

    helper.form_tag = False
    helper.disable_csrf = True

    tags = None  # STUB_TAG


class CommentForm(forms.ModelForm):
    """A short form to submit comments."""
    name = forms.CharField(label="Name:", required=True, max_length=32)
    authors = forms.ModelMultipleChoiceField(label="Authors:", queryset=models.User.objects.all(),
                                             required=False,
                                             widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"))
    tags = forms.ModelMultipleChoiceField(label="Tags:", queryset=models.Tag.objects.all(),
                                          required=False,
                                          widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:tags"))

    helper = FormHelper()
    helper.form_tag = False
    helper.disable_csrf = True