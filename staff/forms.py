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


class HorizontalMixin:
    """A mixin that makes a form display as an inline crispy form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ContentSearchForm(HorizontalMixin, forms.Form):
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


class ContentForm(VerticalMixin, forms.ModelForm):
    """A generic editor for any kind of content."""
    class Meta:
        model = models.Content
        fields = ['title', 'authors', 'guest_authors', 'description', 'embed_only', 'tags', 'section', 'linked']
        widgets = {
            'title': forms.widgets.TextInput(),
            'authors': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:users"),
            'tags': autocomplete.ModelSelect2Multiple(url="staff:autocomplete:tags"),
            'section': autocomplete.ModelSelect2(url="staff:autocomplete:section"),
            'linked': autocomplete.ModelSelect2(url="staff:autocomplete:content")
        }
        abstract = True


class StoryForm(ContentForm):
    """The story editor form."""
    class Meta(ContentForm.Meta):
        model = models.Story
        fields = ContentForm.Meta.fields + ['cover', 'second_deck', 'text']
        widgets = dict(ContentForm.Meta.widgets, text=RichTextWidget(embed=True), lead=RichTextWidget(short=True), cover=autocomplete.ModelSelect2(url='staff:autocomplete:content'))


class GalleryForm(ContentForm):
    """The gallery editor form.

    The actual gallery entry editing takes place outside of this form, which is used to edit
    gallery metadata.
    """
    class Meta(ContentForm.Meta):
        model = models.Gallery


class ContentInsertionForm(HorizontalMixin, forms.Form):
    """A small form for selecting content to add into a gallery."""
    content = forms.ModelChoiceField(
        queryset=models.Content.objects.all(),
        widget=autocomplete.ModelSelect2(url='staff:autocomplete:content')
    )

    class Meta:
        fields = '__all__'


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


class UserSearchForm(HorizontalMixin, forms.Form):
    """Form for searching through content."""
    id = forms.IntegerField(label="ID:", required=False)
    first_name = forms.CharField(label="First Name:", required=False, max_length=100)
    last_name = forms.CharField(label="Last Name:", required=False, max_length=100)
    active = forms.BooleanField(label="Active", required=False)
    graduation_year = forms.IntegerField(label="Graduation Year:", required=False)


class UserManageForm(VerticalMixin, forms.ModelForm):
    """An editor for users and their permissions."""
    verify_password = forms.CharField(label="Verify current password",
                                      help_text="Since this action may be sensitive, we ask you to very your current "
                                                "password.",
                                      widget=forms.PasswordInput())
    new_password = forms.CharField(label="New password",
                                   help_text="Only fill in this field if you wish to change your password.",
                                   widget=forms.PasswordInput(),
                                   required=False)
    confirm_password = forms.CharField(label="Confirm new password",
                                       widget=forms.PasswordInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # save the request so we can check against request.user later
        super().__init__(*args, **kwargs)

    def is_valid(self):
        valid = super().is_valid()

        # Authenticate the user to make sure form submission is authorized
        if not auth.authenticate(username=self.request.user.username, password=self.cleaned_data['verify_password']):
            self._errors['verify_password'] = ["Unauthorized; password is incorrect"]
            valid = False
        # Check that passwords match if passwords are being updated
        if (self.cleaned_data['new_password'] or self.cleaned_data['confirm_password']) and \
                self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            self._errors['confirm_password'] = ["New passwords do not match"]
            valid = False

        return valid

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'groups': forms.CheckboxSelectMultiple()
        }


class UserSelfManageForm(UserManageForm):
    """An editor for users that edits a limited subset of information, available to all users."""
    class Meta:
        model = models.User
        # Override metaclass to only expose name change interface
        fields = ['first_name', 'last_name', 'email']


class ProfileManageForm(VerticalMixin, forms.ModelForm):
    """An editor for profiles, available only to privileged users."""
    class Meta:
        model = models.Profile
        fields = ['biography', 'avatar', 'graduation_year', 'position']


class ProfileSelfManageForm(VerticalMixin, forms.ModelForm):
    """An editor for profiles that edits a limited subset of information, available to all users."""
    class Meta:
        model = models.Profile
        fields = ['biography', 'avatar']
