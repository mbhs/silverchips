"""Script that initializes the default group and permission scheme in development and deployment.

Activate via "python manage.py setuppermissions" or similar.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from core.models import Content, User, Profile, Tag


class Command(BaseCommand):
    help = "Sets up the default group and permission scheme that Silver Chips uses."

    def handle(self, *args, **options):
        # Permissions are associated with particular content types
        content = ContentType.objects.get_for_model(Content)
        user = ContentType.objects.get_for_model(User)
        tag = ContentType.objects.get_for_model(Tag)
        profile = ContentType.objects.get_for_model(Profile)

        # Grant permissions to writers
        writers, _ = Group.objects.get_or_create(name="writers")
        editors, _ = Group.objects.get_or_create(name="editors")
        eics, _ = Group.objects.get_or_create(name="editors-in-chief")
        sponsor, _ = Group.objects.get_or_create(name="sponsors")

        for group in writers, editors, eics, sponsor:
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="draft_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="create_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=profile, codename="edit_profile")
            )
            group.permissions.add(
                Permission.objects.get(content_type=tag, codename="add_tag")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="editown_content")
            )

        for group in editors, eics, sponsor:
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="read_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="edit_content")
            )

        for group in eics, sponsor:
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="publish_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="hide_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="delete_content")
            )
            group.permissions.add(
                Permission.objects.get(content_type=user, codename="manage_users")
            )
            group.permissions.add(
                Permission.objects.get(content_type=content, codename="comment")
            )

        # STUB_COMMENT
