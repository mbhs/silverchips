"""Custom forms.
"""

from django import forms

class CommentForm(forms.Form):
    """ Form for posting comments """

    name = forms.CharField(label="Name", max_length=30)
    text = forms.CharField(label="Text")
