"""Core models for the Silverchips platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
from django.contrib.auth import models as auth
from django.utils import timezone
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import posixpath as path


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

    def __str__(self) -> str:
        """Represent the profile as a string."""

        return "Profile[{}]".format(self.user.get_username())


class ProfileUserManager(auth.UserManager):
    """User manager that handles profile creation."""

    def create_user(self, username, email=None, password=None, **extra_fields) -> User:
        """Override user creation to instantiate a new profile."""

        user = User(username=username, email=email, password=password, **extra_fields)
        profile = Profile(user=user)
        profile.save()
        user.save()
        return user


class User(auth.User):
    """User proxy to override the user manager."""

    objects = ProfileUserManager()

    def __str__(self) -> str:
        """Represent the user as a string.

        This is the value Django Autocomplete Light displays in the
        form element when a user is selected.
        """

        return self.get_full_name()

    def __repr__(self) -> str:
        """Represent the user as a string."""

        return "User[{}]".format(self.get_full_name())

    def get_role(self) -> str or None:
        """Get the user role.

        For now, there are two roles. These are editor and writer.
        Writers are in the lower access tier, and can only upload and
        publish their own stories. Editors can view all stories and
        configure some parts of the site.
        """

        if self.groups.filter(name="editors"):  # or self.is_superuser
            return "editor"
        elif self.groups.filter(name="writers"):
            return "writer"
        return None

    class Meta:
        proxy = True


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """Create the writer and editor roles on database initialization."""

    ContentType.objects.get_or_create(app_label="core", model="site")
    Group.objects.get_or_create(name="writers")
    Group.objects.get_or_create(name="editors")


class TimestampMixin(models.Model):
    """Model mixin for recording creation and edit times.

    Note that this mixin has to have model as a parent because it
    does not have a super to override save on otherwise.
    """

    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Save the model and update the creation and edit times."""

        if not self.created:
            self.created = timezone.now()
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Tag(models.Model):
    """Basic tag model for content."""

    name = models.CharField(max_length=32)


UNPUBLISHED = 0
PENDING = 1
PUBLISHED = 2
HIDDEN = 3


class Content(TimestampMixin):
    """A generic content model.

    This container provides the metaclass for all types of media,
    including stories, images, videos, galleries, and podcasts. Each
    subclass should be capable of rendering itself to HTML so that it
    can be generically displayed or embedded.
    """

    title = models.TextField()
    description = models.TextField()
    authors = models.ManyToManyField(User, related_name="%(class)s_authored")  # user.photo_authored

    # The intent to use a content creator field is to be able to tie
    # content to a registered user if it is authored by, for example,
    # a guest writer outside of Silver Chips. We ultimately decided
    # to drop this functionality because editors can see all content,
    # and so should be in charge of managing external authors.
    # creator = models.ForeignKey(User, related_name="%(class)s_created", on_delete=models.CASCADE)

    # A content can be publishable or unpublishable. This essentially
    # refers to whether or not it is to be made available as a
    # standalone item on the site. For example, stories would always
    # be publishable, whereas a supporting image such as a company
    # logo might not.
    publishable = models.BooleanField(default=True)

    # A publishable content has several states to improve editor
    # workflow. An unpublished story is in progress, whereas a pending
    # story is ready and awaiting editor approval. Once it receives
    # this approval, it is published. If it is desired that the story
    # be taken down, it should be hidden so as to indicate that it at
    # one point passed the publishing process.
    published = models.IntegerField(default=UNPUBLISHED, choices=(
        (UNPUBLISHED, "unpublished"),
        (PENDING, "pending"),
        (PUBLISHED, "published"),
        (HIDDEN, "hidden")))

    tags = models.ManyToManyField(Tag)
    views = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Represent the content as a string."""

        return "Content[{}:{}]".format(type(self).__name__, self.title)

    def has_tag(self, name) -> bool:
        """Check if a model has a tag."""

        return self.tags.filter(name=name).exists()

    class Meta:
        abstract = True
        ordering = ['-created']


# Section names should be pretty
alphanumeric = RegexValidator(r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters and underscore are allowed.")


# For the time being, we are going to move from nested sections to
# path sections. Since the most frequent use case for querying the
# section object is to grab stories for a section, it makes sense to
# use the most efficient database configuration. For a section with
# multiple descendants, a recursive strategy would first have to find
# all descendant sections and then all related stories for each. On
# the other hand, a path configuration would simply filter all stories
# with section paths starting with the given section path.

# class Section(models.Model):
#     """A broad category under which content can be organized."""
#
#     parent = models.ForeignKey("Section", related_name="subsections", null=True, blank=True,
#         on_delete=models.SET_NULL)
#     name = models.CharField(max_length=32, unique=True)
#     title = models.CharField(max_length=64)
#     active = models.BooleanField(default=True)
#
#     def __str__(self) -> str:
#         """Represent the section as a string."""
#
#         return "Sections[{}]".format(self.title)
#
#     def get_ancestors(self) -> ["Section"]:
#         """Get the parent sections of section."""
#
#         ancestors = [self]
#         while ancestors[-1].parent:
#             ancestors.append(ancestors[-1].parent)
#         return ancestors[::-1]
#
#     def get_children(self) -> {"Section"}:
#         """Get the immediate children of the section."""
#
#         return
#
#     def get_descendants(self) -> {"Section"}:
#         """Get all levels of descendants of the section."""
#
#         descendants = {self}
#         if self.subsections.count():
#             for subsection in self.subsections.all():
#                 descendants |= subsection.get_descendants()
#         return descendants
#
#     def all_stories(self):
#         return Story.objects.filter(section__in=self.get_descendants())


class Section(models.Model):
    """All stories are categorized by sections.

    To avoid using a recursive system, sections have an identifying
    string and absolute path. The absolute path is set when the
    """

    name = models.CharField(max_length=32)
    path = models.CharField(max_length=64, unique=True, primary_key=True)
    title = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def assign(self, section: "Section"=None):
        """Assign this section under another section, default to root."""

        if not self.id:
            raise RuntimeError("Section ID is not set.")
        self.path = path.join(path.sep if section is None else section.path, self.name)

    def save(self, *args, **kwargs):
        """Save the section model."""

        if not self.path:
            self.assign()
        super().save(*args, **kwargs)

    def descendants(self):
        """Get all paths under this section."""

        return Section.objects.filter(path__startswith=self.path)

    def children(self):
        """Get paths immediately under this section."""

        depth = self.path.count(path.sep)
        for section in self.descendants():
            if section.count(path.sep) == depth:
                yield section

    def __str__(self):
        """Represent the section as a string."""

        return "Sections[{}]".format(self.title)


class Image(Content):
    """Image subclass for the content model."""

    source = models.ImageField(upload_to="images/%Y/%m/%d/")

    template = "content/image.html"
    descriptor = "Photo"


class Video(Content):
    """Video subclass for the content model."""

    source = models.FileField(upload_to="videos/%Y/%m/%d/")

    template = "content/video.html"
    descriptor = "Video"


class Audio(Content):
    """Audio subclass for the content model."""

    source = models.FileField(upload_to="audio/%Y/%m/%d/")

    template = "content/audio.html"
    descriptor = "Audio"

    class Meta:
        verbose_name_plural = "audio"


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

    template = "content/story.html"
    descriptor = "Story"
    hide_caption = True

    class Meta:
        verbose_name_plural = "stories"
        ordering = ['-created']
