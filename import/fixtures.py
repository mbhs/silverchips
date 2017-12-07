# Generate the database dump with the following command:
#   > mysqldump silverchips --xml -u root -p > /tmp/silverchips.xml

import os
from django import setup
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
setup()

from core.models import Section, Story, User, Profile, Image

OBJ_COUNT = 50
PASSWORD = "abc123"

# Only keep the last 50 stories and 150 images
Story.objects.filter(pk__lt=Story.objects.order_by('-pk')[OBJ_COUNT-1].pk).delete()
Image.objects.filter(pk__lt=Image.objects.order_by('-pk')[3*OBJ_COUNT-1].pk).delete()

# Delete all users with no content
User.objects.filter(Q(story_content=None), Q(image_content=None)).delete()

for user in User.objects.all():
    user.set_password(PASSWORD)
    user.save()