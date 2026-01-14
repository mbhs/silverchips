"""Core models for the Silver Chips platform."""

from django.db import models
import django.contrib.auth.models as auth
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.urls import reverse
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel
from captcha.fields import CaptchaField

import PIL.Image
import PIL.ExifTags


def new_student_grad_year():
    return timezone.now().year + 4


class Profile(models.Model):
    """The profile model provides non-authentication/identification information about users.

    When a new user object is instantiated, a profile object is
    immediately created and assigned to them. Note that roles are
    stored by Django groups instead of in members of the class.
    """

    # Associate this Profile with a particular User
    user = models.OneToOneField(
        "User", related_name="profile", on_delete=models.CASCADE
    )

    # Personal information
    biography = models.TextField(
        help_text="A short biography, often including likes and dislikes, accomplishments,"
        " etc. Should be several sentences minimum."
    )
    avatar = models.ImageField(blank=True, null=True)
    position = models.TextField()
    graduation_year = models.IntegerField(
        default=new_student_grad_year
    )  # force recalculation
    is_hidden = models.BooleanField(
        default=False, help_text="Whether or not to hide this user from /about/staff"
    )

    def __str__(self):
        """Represent the profile as a string."""

        return "Profile[{}]".format(self.user.get_username())

    class Meta:
        # Create permissions for Profile objects
        permissions = (("edit_profile", "Can edit one's own user profile"),)


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
        permissions = (("manage_users", "Can manage user data and privileges"),)
        ordering = ("-profile__graduation_year", "last_name")


class Tag(models.Model):
    """Basic tag model for content."""

    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        """Represent the tag as a string.

        This is the value Django Autocomplete Light displays in the
        form element when a tag is selected.
        """
        return self.name


class Content(PolymorphicModel):
    """A generic content model.

    This container provides the metaclass for all types of media,
    including stories, images, videos, galleries, and podcasts. Each
    subclass should be capable of rendering itself to HTML so that it
    can be generically displayed or embedded. States pertaining to editing and publishing
    status are also stored.
    """

    # Basic identification information
    title = models.TextField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    legacy_id = models.IntegerField(null=True, blank=True)

    # Time information
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    # Authorship information
    authors = models.ManyToManyField(
        User, related_name="%(class)s_authored", blank=True
    )  # user.images_authored
    guest_authors = models.CharField(
        max_length=64, default="", blank=True
    )  # Authors who aren't in the database
    uploader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="uploaded_content",
        blank=True,
        null=True,
    )  # The person who uploaded the content

    # Tracking information
    section = models.ForeignKey(
        "Section",
        related_name="content",
        on_delete=models.CASCADE,
    )
    views = models.IntegerField(default=0)

    # Whether this content should show up by itself
    embed_only = models.BooleanField(
        default=False,
        help_text="Whether this content should be used only in the context"
        " of embedding into other content (especially stories), or whether it should"
        " appear independently on the site. You will often mark content as embed only"
        " when it is not original or when it is meaningless outside of some"
        " broader story.",
    )

    # Linked content
    linked = models.ManyToManyField("Content", blank=True)

    # Content visibility workflow constants
    DRAFT = 1
    PENDING = 2
    PUBLISHED = 3
    HIDDEN = 0

    visibility = models.IntegerField(
        default=DRAFT,
        choices=(
            (DRAFT, "draft"),
            (PENDING, "pending"),
            (PUBLISHED, "published"),
            (HIDDEN, "hidden"),
        ),
    )

    @property
    def type(self):
        """Helper function to find the particular subclass type name of this Content."""
        return type(self).__name__

    @property
    def slug(self):
        """Return a slugified version of this Content's title for use in URLs."""
        return slugify(self.title)

    def __repr__(self):
        """Represent this Content as a string."""
        return "Content[{}:{}]".format(self.type, self.title)

    def has_tag(self, name):
        """Check if this Content has a particular Tag."""

        return self.tags.filter(name=name).exists()

    def is_owned_by(self, user):
        """Check if this Content is owned by a particular User (author or uploader)."""
        return self.uploader == user or self.authors.filter(pk=self.pk).exists()

    def has_authors(self):
        """Check if this Content has any authors or guest authors."""
        return self.authors.exists() or self.guest_authors.strip() != ""

    class Meta:
        ordering = ["-created"]
        permissions = (
            ("draft_content", "Can draft content"),
            ("edit_content", "Can edit content"),
            ("read_content", "Can read all content"),
            ("publish_content", "Can publish content"),
            ("hide_content", "Can hide content"),
            ("create_content", "Can create content"),
            ("editown_content", "Can edit self-authored content"),
            ("comment", "Can manage comments"),
        )

    def get_absolute_url(self):
        """Find the URL through which this Content can be accessed."""
        return reverse(
            "home:view_content", args=[self.slug, self.pk] if self.slug else [self.pk]
        )


# Section names should be pretty
alphanumeric = RegexValidator(
    r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters and underscore are allowed."
)


class Section(models.Model):
    """A Content category under which Content can be organized."""

    parent = models.ForeignKey(
        "self",
        related_name="subsections",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        max_length=32, unique=True
    )  # Internal tracking name (used in URLs)
    title = models.CharField(max_length=64)  # External name for display

    visible = models.BooleanField(
        default=True
    )  # Whether this section should show up on the site

    NONE = -1
    DENSE = 0
    COMPACT = 1
    LIST = 2
    FEATURES = 3
    MAIN = 4

    index_display = models.IntegerField(
        default=NONE,
        choices=(
            (NONE, "-1"),
            (DENSE, "dense"),
            (COMPACT, "compact"),
            (LIST, "list"),
            (FEATURES, "features"),
            (MAIN, "main"),
        ),
    )

    priority = models.IntegerField(default=NONE, null=True)

    def __str__(self):
       """Represent this Section as a string."""
       if self.priority != -1:
           return f'{self.title} ({self.priority})'
       return self.title

    def get_ancestors(self):
        """Get all Sections that are ancestors of this Section."""
        ancestors = [self]

        # Continually scale the ladder of parenthood
        while ancestors[-1].parent:
            ancestors.append(ancestors[-1].parent)

        return ancestors[::-1]

    def get_descendants(self):
        """Get all Sections that are descendants of this Section."""
        descendants = {self}

        # Continually descend the tree of childhood recursively
        if self.subsections.count():
            for subsection in self.subsections.all():
                descendants |= subsection.get_descendants()

        return descendants

    def all_content(self):
        """Get all the Content that belongs to this Section for display in section templates."""
        return Content.objects.filter(
            visibility=Content.PUBLISHED,
            embed_only=False,
            section__in=self.get_descendants(),
        )

    def is_root(self):
        """Check whether this Section is a root Section."""
        return self.parent is None

    def get_absolute_url(self):
        """Find the URL through which this Section can be accessed."""
        return reverse("home:view_section", args=[self.name])

    class Meta:
        verbose_name_plural = "sections"
        ordering = ["priority"]

class Image(Content):
    """Image subclass for the Content model."""

    source = models.ImageField(upload_to="images/%Y/%m/%d/")

    template = "home/content/image.html"
    sidebar_template = "home/content/sidebars/image.html"
    descriptor = "Photo"

    def exif_data(self):
        try:
            _image = PIL.Image.open(self.source.file)
            exif = {
                PIL.ExifTags.TAGS[exif_tag]: value
                for exif_tag, value in _image._getexif().items()
                if exif_tag in PIL.ExifTags.TAGS
            }
            return exif
        # SyntaxError is for corrupted images
        except (FileNotFoundError, AttributeError, SyntaxError) as e:
            return None

class Art(Content):
    """Image subclass for the Content model."""

    source = models.ImageField(upload_to="images/%Y/%m/%d/")

    template = "home/content/art.html"
    sidebar_template = "home/content/sidebars/image.html"
    descriptor = "Art"
    cover = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL
    )  # Cover photo
    def exif_data(self):
        try:
            _image = PIL.Image.open(self.source.file)
            exif = {
                PIL.ExifTags.TAGS[exif_tag]: value
                for exif_tag, value in _image._getexif().items()
                if exif_tag in PIL.ExifTags.TAGS
            }
            return exif
        # SyntaxError is for corrupted images
        except (FileNotFoundError, AttributeError, SyntaxError) as e:
            return None

class Video(Content):
    """Video subclass for the Content model."""

    source = models.FileField(upload_to="videos/%Y/%m/%d/")
    cover = models.ForeignKey(
        Image, null=True, on_delete=models.SET_NULL
    )  # Cover photo

    template = "home/content/video.html"
    descriptor = "Video"


class Audio(Content):
    """Audio subclass for the Content model."""

    source = models.FileField(upload_to="audio/%Y/%m/%d/")

    template = "home/content/audio.html"
    descriptor = "Audio"


class Poll(Content):
    pass  # STUB_POLL


class Story(Content):
    """The main story model."""

    second_deck = models.TextField()  # Second deck
    text = models.TextField()  # Full text
    cover = models.ForeignKey(
        Image, null=True, on_delete=models.SET_NULL
    )  # Cover photo

    template = "home/content/story.html"
    descriptor = "Story"
    hide_caption = True

    class Meta:
        verbose_name_plural = "stories"


class Gallery(Content):
    """A model representing an ordered gallery of other Content."""

    entries = models.ManyToManyField(
        Content, through="core.GalleryEntryLink", related_name="containing_galleries"
    )

    template = "home/content/gallery.html"
    descriptor = "Gallery"
    hide_caption = True

    def entries_in_order(self):
        return self.entries.order_by("gallery_links")


class GalleryEntryLink(OrderedModel):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="entry_links"
    )
    entry = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="gallery_links"
    )
    order_with_respect_to = "gallery"

    class Meta:
        ordering = ("gallery", "order")


class Comment(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField()
    captcha = CaptchaField()
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, null=True, related_name="comments"
    )
    date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    VISIBLE = 2
    HIDDEN = 3

    class Meta:
        ordering = ("date",)


class Search(models.Model):
    search = models.CharField(max_length=200)
    text = models.TextField()


class Breaking(models.Model):
    content = models.ForeignKey(
        "Content",
        related_name="breaking_content",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class Banner(models.Model):
    priority = models.PositiveSmallIntegerField()
    url = models.CharField(max_length=2048)
    text = models.CharField(max_length=500)
