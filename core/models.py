"""Core models for the Silverchips platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
import django.contrib.auth.models as auth
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.urls import reverse
from polymorphic.models import PolymorphicModel


class Profile(models.Model):
    """The profile model provides more information about users.

    When a new user object is instantiated, a profile object is
    immediately created and assigned to them. Note that roles are
    stored by Django groups instead of in members of the class.

    Keep in mind that this profile will eventually be replaced by a
    OpenID backend model which will allow for synchronization with
    the main MBHS site.
    """

    user = models.OneToOneField("User", related_name="profile", on_delete=models.CASCADE)

    # Personal information
    biography = models.TextField()
    avatar = models.ForeignKey("Image", blank=True, null=True, on_delete=models.SET_NULL)
    position = models.TextField()
    graduation_year = models.IntegerField()
    active = models.BooleanField(default=True)

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

    def __str__(self):
        """Represent the user as a string.

        This is the value Django Autocomplete Light displays in the
        form element when a user is selected.
        """
        return self.get_full_name()

    def __repr__(self):
        """Represent the user as a string."""

        return "User[{}]".format(self.get_full_name())

    class Meta:
        proxy = True


class Tag(models.Model):
    """Basic tag model for content."""

    name = models.CharField(max_length=32)


class Content(PolymorphicModel):
    """A generic content model.

    This container provides the metaclass for all types of media,
    including stories, images, videos, galleries, and podcasts. Each
    subclass should be capable of rendering itself to HTML so that it
    can be generically displayed or embedded.
    """

    title = models.TextField()
    description = models.TextField()
    authors = models.ManyToManyField(User, related_name="%(class)s_authored")  # user.image_authored

    # A content can be publishable or unpublishable. This essentially
    # refers to whether or not it is to be made available as a
    # standalone item on the site. For example, stories would always
    # be publishable, whereas a supporting image such as a company
    # logo might not.
    publishable = models.BooleanField(default=True)

    # A publishable content has several states to improve editor
    # workflow. An draft story is in progress, whereas a pending
    # story is ready and awaiting editor approval. Once it receives
    # this approval, it is published. If it is desired that the story
    # be taken down, it should be hidden so as to indicate that it at
    # one point passed the publishing process.

    DRAFT = 1
    PENDING = 2
    PUBLISHED = 3
    HIDDEN = 0

    visibility = models.IntegerField(default=DRAFT, choices=(
        (DRAFT, "draft"),
        (PENDING, "pending"),
        (PUBLISHED, "published"),
        (HIDDEN, "hidden")))

    tags = models.ManyToManyField(Tag)
    views = models.IntegerField(default=0)

    legacy_id = models.IntegerField(null=True)

    @property
    def type(self):
        return type(self).__name__

    @property
    def slug(self):
        return slugify(self.title)

    def __str__(self):
        """Represent the content as a string."""

        return "Content[{}:{}]".format(self.type, self.title)

    def has_tag(self, name):
        """Check if a model has a tag."""

        return self.tags.filter(name=name).exists()

    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
        permissions = (
            ('draft_content', "Can draft content"),
            ('edit_content', "Can edit content"),
            ('read_content', "Can read all content"),
            ('publish_content', "Can publish content"),
            ('hide_content', "Can hide content")
        )

    def get_absolute_url(self):
        return reverse('home:view_content', args=[self.slug, self.pk])


# Section names should be pretty
alphanumeric = RegexValidator(r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters and underscore are allowed.")


class Section(models.Model):
    """A broad category under which content can be organized."""

    parent = models.ForeignKey("self", related_name="subsections", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Sections[{}]'.format(self.title)

    def get_ancestors(self):
        ancestors = [self]
        while ancestors[-1].parent:
            ancestors.append(ancestors[-1].parent)
        return ancestors[::-1]

    def get_descendants(self):
        descendants = {self}
        if self.subsections.count():
            for subsection in self.subsections.all():
                descendants |= subsection.get_descendants()
        return descendants

    def all_stories(self):
        return Story.objects.filter(visibility=Content.PUBLISHED, section__in=self.get_descendants())

    def is_root(self):
        return 

    class Meta:
        verbose_name_plural = "sections"


# class Section(models.Model):
#     """All stories are categorized by sections.
#
#     To avoid using a recursive system, sections have an identifying
#     string and absolute path. The absolute path is set when the
#     """
#
#     id = models.CharField(max_length=16, validators=[alphanumeric])
#     _path = models.CharField(max_length=64, unique=True, primary_key=True)
#
#     name = models.CharField(max_length=32)
#     title = models.CharField(max_length=64)
#     active = models.BooleanField(default=True)
#
#     def assign(self, section: "Section"=None):
#         """Assign this section under another section."""
#
#         if not self.id:
#             raise RuntimeError("Section ID is not set.")
#         if section is None:
#             self._path = "/" + self.id
#         else:
#             self._path = posixpath.join(section.path, self.id)
#
#     def save(self, *args, **kwargs):
#         """Save the section model.
#
#         If the path is not set, the section is automatically assigned
#         to the root path.
#         """
#
#         if not self._path:
#             self.assign()
#         super().save(*args, **kwargs)
#
#     @property
#     def path(self):
#         """Get the path to the section."""
#
#         return self._path
#
#     def __str__(self):
#         """Represent the section as a string."""
#
#         return "Sections[{}]".format(self.title)


class Image(Content):
    """Image subclass for the content model."""

    source = models.ImageField(upload_to="images/%Y/%m/%d/")

    template = "home/content/image.html"
    descriptor = "Photo"


class Video(Content):
    """Video subclass for the content model."""

    source = models.FileField(upload_to="videos/%Y/%m/%d/")

    template = "home/content/video.html"
    descriptor = "Video"


class Audio(Content):
    """Audio subclass for the content model."""

    source = models.FileField(upload_to="audio/%Y/%m/%d/")

    template = "home/content/audio.html"
    descriptor = "Audio"


class Story(Content):
    """The main story model.

    Stories are the backbone of a news site, and are one of the most
    important models. In addition to storing information relating to
    the written contents, states pertaining to editing and publishing
    status are also stored.
    """

    lead = models.TextField()
    text = models.TextField()

    section = models.ForeignKey(Section, related_name="stories", null=True, on_delete=models.SET_NULL)
    cover = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL)

    template = "home/content/story.html"
    descriptor = "Story"
    hide_caption = True

    class Meta:
        verbose_name_plural = "stories"
        ordering = ['-created']
