"""Custom forms for the staff interface."""
from django import forms
from django.contrib import auth
from dal import autocomplete
from crispy_forms.helper import FormHelper

from core import models
from staff.widgets import RichTextWidget


class LoginForm(forms.Form):
    """A basic login form for staff and administrators."""
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password")


class VerticalMixin:
    """A mixin that makes a form display as a vertically organized crispy form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


class SearchMixin:
    """A mixin that makes a form display as an inline crispy form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ContentSearchForm(SearchMixin, forms.Form):
    """Form for searching through content."""
    id = forms.IntegerField(label="ID:", required=False)
    title = forms.CharField(label="Title:", required=False, max_length=100)
    after = forms.DateField(label="Created After:", required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    before = forms.DateField(label="Created Before:", required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    authors = forms.ModelMultipleChoiceField(label="Authors:", queryset=models.User.objects.all(),
                                             required=False,
                                             widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"))
    tags = forms.ModelMultipleChoiceField(label="Tags:", queryset=models.Tag.objects.all(),
                                          required=False,
                                          widget=autocomplete.ModelSelect2Multiple(url="staff:autocomplete:tags"))

    helper = FormHelper()
    helper.form_tag = False
    helper.disable_csrf = True
    # type = forms.ModelMultipleChoiceField(label=)


class ContentForm(VerticalMixin, forms.ModelForm):
    """A generic editor for any kind of content."""
    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'guest_authors', 'description', 'embed_only', 'tags']
        widgets = {
            'title': forms.widgets.TextInput(),
            'description': RichTextWidget(short=True),
            'authors': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"),
            'tags': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:tags")
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


class VideoForm(ContentForm):
    """Form for video creation."""
    class Meta(ContentForm.Meta):
        model = models.Video
        fields = ContentForm.Meta.fields + ['source']


class AudioForm(ContentForm):
    """Form for audio creation."""
    class Meta(ContentForm.Meta):
        model = models.Audio
        fields = ContentForm.Meta.fields + ['source']


class PollForm(ContentForm):
    pass
    # STUB_POLL


class UserSearchForm(SearchMixin, forms.Form):
    """Form for searching through content."""
    id = forms.IntegerField(label="ID:", required=False)
    first_name = forms.CharField(label="First Name:", required=False, max_length=100)
    last_name = forms.CharField(label="Last Name:", required=False, max_length=100)
    active = forms.BooleanField(label="Active", required=False)
    graduation_year = forms.IntegerField(label="Graduation Year:", required=False)


class UserManageForm(VerticalMixin, forms.ModelForm):
    """An editor for users and their permissions."""
    verify_password = forms.CharField(label="Verify password",
                                      help_text="Since this action may be sensitive, we ask you to very your current "
                                                "password.",
                                      widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'groups', 'is_active']
        widgets = {
            'groups': forms.CheckboxSelectMultiple()
        }

    def is_valid(self):
        valid = super().is_valid()
        if not auth.authenticate(username=self.request.user.username, password=self.cleaned_data['verify_password']):
            self._errors['verify_password'] = ["Password was incorrect"]
            return False
        return valid


class ProfileManageForm(VerticalMixin, forms.ModelForm):
    """An editor for profiles, available only to privileged users."""
    class Meta:
        model = models.Profile
        fields = ['biography', 'avatar', 'graduation_year', 'position']
