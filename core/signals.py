from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.models import Content


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """Create the writer and editor roles on database initialization."""

    ContentType.objects.get_or_create(app_label="core", model="site")
    Group.objects.get_or_create(name="writers")
    Group.objects.get_or_create(name="editors")
