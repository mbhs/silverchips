# Generate the database dump with the following command:
#     mysqldump silverchips --xml -u root -p > /tmp/silverchips.xml

import os
from django import setup
from xml.etree import ElementTree as et
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")

setup()

from core.models import Section, Story, User, Profile

Section.objects.all().delete()
Story.objects.all().delete()
User.objects.all().delete()
Profile.objects.all().delete()

with open("import/silverchips.xml", 'r', encoding="latin-1", errors="replace") as xml_file:
    xml_data = xml_file.read()

# Eliminate special characters (except the newline)
for x in range(32):
    if x != 10:
        xml_data = xml_data.replace(chr(x), "")

# TODO: expand/check this
xml_data = xml_data.replace("\x85", "!")
xml_data = xml_data.replace("\x91", "'")
xml_data = xml_data.replace("\x92", "'")
xml_data = xml_data.replace("\x93", "\"")
xml_data = xml_data.replace("\x94", "\"")
xml_data = xml_data.replace("&amp;#39;", "'")
xml_data = xml_data.replace("&amp;#34;", "\"")
xml_data = xml_data.replace("\x97", "—")

print("Sanitized control characters.")

root = et.fromstring(xml_data)
print("Parsed XML data.")


def read_table(table):
    return root.find("./database/table_data[@name='{}']".format(table))


def get_field(row, field, default=None):
    entry = row.find("./field[@name='{}']".format(field))

    return entry.text if entry is not None and entry.text else default


def read_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

users = read_table("user")

# for i, old_user in enumerate(users):
#     user_id = int(get_field(old_user, "id"))
#     user = User(id=user_id,
#                 username=get_field(old_user, "uname", "") + "_old" + str(user_id),
#                 first_name=get_field(old_user, "fname", "(no first name)"),
#                 last_name=get_field(old_user, "lname", "(no last name)"))
#     user.save()
# 
#     profile = Profile(id=user_id,
#                       user=user,
#                       biography=get_field(old_user, "bio", "(no biography)"))
#     profile.save()

categories = read_table("category")

for old_category in categories:
    parent_id = int(get_field(old_category, "pid"))
    section = Section(id=get_field(old_category, "id"),
                        parent=(Section.objects.get(id=parent_id) if parent_id > 0 else None),
                        name=get_field(old_category, "url_name"),
                        title=get_field(old_category, "name"))
    section.save()

stories = read_table("story")

for i, old_story in enumerate(stories):
    try:
        category_id = int(get_field(old_story, "cid"))
        date = read_date(get_field(old_story, "date"))
        story = Story(id=get_field(old_story, "sid"),
                      title=get_field(old_story, "headline", "(no title)"),
                      description=get_field(old_story, "secdeck", "(no description)"),
                      lead=get_field(old_story, "lead", "(no lead)"),
                      text=get_field(old_story, "text", "(no text)"),
                      section=(Section.objects.get(id=category_id) if category_id > 0 else None),
                      created=date,
                      modified=date)
        story.save()
    except:
        print("Failed to import story {}/{}".format(i, len(stories)))


for link in read_table("story_author"):
    story = Story.objects.get(id=int(get_field(link, "sid")))
    story.authors.add(User.objects.get(id=int(get_field(link, "uid"))))
    story.save()