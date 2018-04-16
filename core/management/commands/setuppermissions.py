from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from core.models import Content


class Command(BaseCommand):
    help = 'Sets up the default group and permission scheme that SilverChips uses.'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Content)

        writers, _ = Group.objects.get_or_create(name="writers")
        writers.permissions.add(Permission.objects.get(content_type=content_type, codename='draft_content'))

        editors, _ = Group.objects.get_or_create(name="editors")
        editors.permissions.add(Permission.objects.get(content_type=content_type, codename='read_content'))
        editors.permissions.add(Permission.objects.get(content_type=content_type, codename='edit_content'))

        eics, _ = Group.objects.get_or_create(name="editors-in-chief")
        eics.permissions.add(Permission.objects.get(content_type=content_type, codename='publish_content'))
        eics.permissions.add(Permission.objects.get(content_type=content_type, codename='hide_content'))
        eics.permissions.add(Permission.objects.get(content_type=content_type, codename='delete_content'))
