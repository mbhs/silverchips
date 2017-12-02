"""Core models for the Silverchips platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
import django.contrib.auth.models as auth
from django.utils import timezone
from django.core.validators import RegexValidator

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import posixpath


class TimeTrackingModel(models.Model):
    """Model mixin for recording creation and edit times."""

    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Save the model and update the creation and edit times."""

        if not self.created:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Content(TimeTrackingModel):
    """A generic content model.

    This container provides the metaclass for all types of media,
    including stories, images, videos, galleries, and podcasts. Each
    subclass should be capable of rendering itself to HTML so that it
    can be generically displayed or embedded.
    """

    title = models.TextField()
    description = models.TextField()
    authors = models.ManyToManyField("User", related_name="%(class)s_content")  # user.photo_content

    views = models.IntegerField(default=0)

    def __str__(self):
        """Represent the content as a string."""

        return "Content[{}:{}]".format(type(self).__name__, self.title)

    class Meta:
        abstract = True
        order_with_respect_to = "created"


# Section names should be pretty
alphanumeric = RegexValidator(r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters and underscore are allowed.")


class Section(models.Model):
    """All stories are categorized by sections.

    To avoid using a recursive system, sections have an identifying
    string and absolute path. The absolute path is set when the
    """

    id = models.CharField(max_length=16, validators=[alphanumeric])
    _path = models.CharField(max_length=64, unique=True, primary_key=True)

    name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def assign(self, section: "Section"=None):
        """Assign this section under another section."""

        if not self.id:
            raise RuntimeError("Section ID is not set.")
        if section is None:
            self._path = "/" + self.id
        else:
            self._path = posixpath.join(section.path, self.id)

    def save(self, *args, **kwargs):
        """Save the section model.

        If the path is not set, the section is automatically assigned
        to the root path.
        """

        if not self._path:
            self.assign()
        super().save(*args, **kwargs)

    @property
    def path(self):
        """Get the path to the section."""

        return self._path

    def __str__(self):
        """Represent the section as a string."""

        return "Sections[{}]".format(self.title)


class Profile(models.Model):
    """The profile model provides more information about users.

    When a new user object is instantiated, a profile object is
    immediately created and assigned to them. Note that roles are
    stored by Django groups instead of in members of the class.

    Keep in mind that this profile will eventually be replaced by a
    OpenID backend model which will allow for synchronization with
    the main MBHS site.
    """

    user = models.OneToOneField("User", related_name="profile")

    # Personal information
    biography = models.TextField()
    avatar = models.ImageField(null=True)

    def __str__(self):
        """Represent the profile as a string."""

        return "Profile[{}]".format(self.user.get_username())


class ProfileUserManager(auth.UserManager):
    """User manager that handles profile creation."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Override user creation to instantiate a new profile."""

        user = User(username=username, email=email, password=password, **extra_fields)
        profile = Profile(user=user)
        profile.save()
        user.save()

        return user


class User(auth.User):
    """User proxy to override the user manager."""

    objects = ProfileUserManager()

    class Meta:
        proxy = True


site = ContentType.objects.get_or_create(app_label="core", model="site")
writers = Group.objects.get_or_create(name="Writers")
editors = Group.objects.get_or_create(name="Editors")


# Some publishing pipeline constants
UNPUBLISHED = 0
PENDING = 1
PUBLISHED = 2
HIDDEN = 3


class PublishingPipelineMixin:
    """Provides state variables for content that is published.

    This mixin gives clarity to where content is in the publishing
    process. It can be unpublished, pending, published, and hidden.
    Pending is intended for authors to indicate that their content
    is ready to be published, though may not be used. Hidden is for
    authors to take down published work.
    """

    publishable = True
    published = models.IntegerField(default=0, choices=(
        (0, "unpublished"),
        (1, "pending"),
        (2, "published"),
        (3, "hidden")))


class Image(Content):
    source = models.ImageField(upload_to="uploads/images/")

    template = "content/image.html"
    descriptor = "Photo"


class Story(Content, PublishingPipelineMixin):
    """The main story model.

    Stories are the backbone of a news site, and are one of the most
    important models. In addition to storing information relating to
    the written contents, states pertaining to editing and publishing
    status are also stored.
    """

    lead = models.TextField()
    text = models.TextField()

    cover = models.ForeignKey(Image, null=True)
    section = models.ForeignKey(Section, related_name="stories", null=True)

    template = "content/story.html"
    descriptor = "Story"

    class Meta:
        verbose_name_plural = "stories"
