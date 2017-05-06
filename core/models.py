"""Core models for the Django News platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import os


# Base classes
class Content(models.Model):
    """A generic model that tracks creation and edit times.

    The corresponding times are updated when save is called. Whether
    the object has been created is determined by if it has an ID.
    """
    
    # Created and modified timestamps
    created = models.DateTimeField()
    modified = models.DateTimeField()

    description = models.TextField()
    title = models.TextField()
    authors = models.ManyToManyField(User, related_name="%(class)s_content")

    views = models.IntegerField()

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


# Account models
class Profile(models.Model):
    """The base user profile class.

    Represents a website writer, editor, or administrator. Has an auto
    index field use as a foreign key.
    """

    # Link to an authenticated user
    user = models.ForeignKey(User, related_name="profile")

    # Personal information
    biography = models.TextField()
    avatar = models.ForeignKey("Image", on_delete=models.CASCADE, null=True)


class Image(Content):
    """Image model."""

    image = models.ImageField()


class Story(Content):
    """The integrated story model.

    Story models do not track the media types they contain. Instead,
    this information is managed directly by the HTML of story text.
    """

    # Core story fields
    lead = models.TextField()
    content = models.TextField()
