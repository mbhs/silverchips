"""Core models for the Django News platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
from django.contrib.auth import models as amodels
from django.utils import timezone


# Base classes
class TimestampedModel(models.Model):
    """A generic model that tracks creation and edit times.

    The corresponding times are updated when save is called. Whether
    the object has been created is determined by if it has an ID.
    """
    
    # Created and modified timestamps
    created = models.DateTimeField()
    modified = models.DateTimeField()

    # Save overload
    def save(self, *args, **kwargs):
        """Save the model and update timestamps.

        If the model does not have an ID, it is assumed that it has not
        been saved, and therefore that the created time should be set.
        The edited time is always updated.
        """

        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)
    
    # Make this model abstract: you can't actually instantiate it
    class Meta:
        abstract = True


# Base content model
class Content(TimestampedModel):
    """The core content class.

    Maintains signature information, activity, and visibility. Also
    provides framework for customized subclasses.
    """

    # Status
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    # Make this model abstract: you can't actually instantiate it
    class Meta:
        abstract = True

# Account models
class User(amodels.User, TimestampedModel):
    """The base user class. 

    Represents a website writer, editor, or administrator. Has an auto
    index field use as a foreign key.
    """

    # Personal information
    biography = models.TextField()
    avatar = models.ForeignKey("Image", on_delete=models.CASCADE, null=True)


# Raw media models
class Media(Content):
    """Generic media item.

    This class is extended to images, audio clips, and videos, all of
    which will be able to be integrated in more advanced media models.
    """

    # Name information
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=300)
    description = models.CharField(max_length=500)

    # Tracking uploader
    uploader = models.ForeignKey("User", on_delete=models.CASCADE)
    
    # Make this model abstract: you can't actually instantiate it
    class Meta:
        abstract = True



# Multimedia or posted content
class Multimedia(Media):
    """The integrated multimedia model.

    This is the base class for developed media structures, such as
    stories and galleries.
    """

    def get_upload_to(self, filename):
        return None
    
    # Source file
    source = models.FileField(upload_to=lambda i,f: i.get_upload_to(f))
    
    # Make this model abstract: you can't actually instantiate it
    class Meta:
        abstract = True


class Image(Multimedia):
    """Image model."""

    def get_upload_to(self, filename):
        return "images/" + filename


class Audio(Multimedia):
    """Audio model."""

    def get_upload_to(self, filename):
        return "audio/" + filename


class Video(Multimedia):
    """Raw video model."""

    def get_upload_to(self, filename):
        return "video/" + filename


class Story(Media):
    """The integrated story model.

    Story models do not track the media types they contain. Instead,
    this information is managed directly by the HTML of story text.
    """

    # Core story fields
    lead = models.TextField()
    content = models.TextField()

