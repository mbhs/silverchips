"""Core models for the Silverchips platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

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
    authors = models.ManyToManyField(User, related_name="%(class)s_content")  # user.photo_content

    views = models.IntegerField(default=0)

    def __str__(self):
        """Represent the content as a string."""

        return 'Content[{}:{}]'.format(type(self).__name__, self.title)

    class Meta:
        abstract = True
        order_with_respect_to = 'created'


# Section names should be pretty
alphanumeric = RegexValidator(r'^[a-zA-Z0-9_]*$', 'Only alphanumeric characters and underscore are allowed.')


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

        return 'Sections[{}]'.format(self.title)


class Profile(models.Model):
    # Link to an authenticated user
    user = models.OneToOneField(User, related_name="profile")

    # Personal information
    biography = models.TextField()
    avatar = models.ImageField(null=True)

    def __str__(self):
        return 'Profile[{}]'.format(self.user.get_username())


class Image(Content):
    source = models.ImageField(upload_to="uploads/images/")

    template = "content/image.html"
    descriptor = "Photo"


class Story(Content):
    lead = models.TextField()
    text = models.TextField()

    cover = models.ForeignKey(Image, null=True)
    section = models.ForeignKey(Section, related_name="stories", null=True)

    template = "content/story.html"
    descriptor = "Story"

    class Meta:
        verbose_name_plural = "stories"
