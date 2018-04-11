# Generate the database dump with the following command:
#   > mysqldump silverchips --xml -u root -p > /tmp/silverchips.xml

import os
from django import setup
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
setup()

from core.models import Section, Story, User, Profile, Image, PUBLISHED
from django.contrib.auth.models import Group

OBJ_COUNT = 50
PASSWORD = "abc123"

Story.objects.filter(authors=None).delete()
Image.objects.filter(authors=None).delete()

# Only keep the last 50 stories
Story.objects.filter(pk__lt=Story.objects.order_by('-pk')[OBJ_COUNT-1].pk).delete()
for story in Story.objects.all():
    story.published = PUBLISHED
    story.save()

# Only keep the last 50 images
Image.objects.filter(pk__lt=Image.objects.order_by('-pk')[3*OBJ_COUNT-1].pk).delete()

# Delete all users with no content
User.objects.filter(Q(content_authored=None)).delete()

for user in User.objects.all():
    user.username = user.username.split("_")[0]
    user.set_password(PASSWORD)
    print(user.username)

    if not User.objects.filter(username=user.username).exists():
        user.save()

User.objects.get(pk=909).groups.add(Group.objects.get(name='editors'))
User.objects.get(pk=908).groups.add(Group.objects.get(name='editors'))
