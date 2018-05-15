"""Script that initializes the default group and permission scheme in development and deployment.

Activate via "python manage.py setuppermissions" or similar.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from core.models import Content, User, Profile


class Command(BaseCommand):
    help = 'Sets up the default group and permission scheme that SilverChips uses.'

    def handle(self, *args, **options):
        # Permissions are associated with particular content types
        content = ContentType.objects.get_for_model(Content)
        user = ContentType.objects.get_for_model(User)
        profile = ContentType.objects.get_for_model(Profile)

        # Grant permissions to writers
        writers, _ = Group.objects.get_or_create(name="writers")
        writers.permissions.add(Permission.objects.get(content_type=content, codename='draft_content'))
        writers.permissions.add(Permission.objects.get(content_type=content, codename='create_content'))
        writers.permissions.add(Permission.objects.get(content_type=profile, codename='edit_profile'))

        # Grant permissions to editors
        editors, _ = Group.objects.get_or_create(name="editors")
        editors.permissions.add(Permission.objects.get(content_type=content, codename='read_content'))
        editors.permissions.add(Permission.objects.get(content_type=content, codename='edit_content'))

        # Grand permissions to editors-in-chief
        eics, _ = Group.objects.get_or_create(name="editors-in-chief")
        eics.permissions.add(Permission.objects.get(content_type=content, codename='publish_content'))
        eics.permissions.add(Permission.objects.get(content_type=content, codename='hide_content'))
        eics.permissions.add(Permission.objects.get(content_type=content, codename='delete_content'))
        eics.permissions.add(Permission.objects.get(content_type=user, codename='manage_users'))
