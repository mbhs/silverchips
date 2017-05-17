"""Core models for the Django News platform.

The full model documentation is located in `/docs/models.md`. Details
about models in the previous platform are located there as well.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Content(models.Model):
    # Created and modified timestamps
    created = models.DateTimeField()
    modified = models.DateTimeField()

    description = models.TextField()
    title = models.TextField()
    authors = models.ManyToManyField(User, related_name="%(class)s_content")

    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        self.modified = timezone.now()

        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Content[{}:{}]'.format(type(self).__name__, self.title)

    class Meta:
        abstract = True
        order_with_respect_to = 'created'


class Category(models.Model):
    parent = models.ForeignKey("self", related_name="subcategories", null=True, blank=True)

    name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)

    display = models.BooleanField(default=True)

    def __str__(self):
        return 'Category[{}]'.format(self.title)


class Profile(models.Model):
    # Link to an authenticated user
    user = models.OneToOneField(User, related_name="profile")

    # Personal information
    biography = models.TextField()
    avatar = models.ForeignKey("Image", on_delete=models.CASCADE, null=True)


class Image(Content):
    source = models.ImageField()


class Story(Content):
    lead = models.TextField()
    content = models.TextField()

    cover = models.ForeignKey(Image, null=True)
    category = models.ForeignKey(Category, related_name="stories")
