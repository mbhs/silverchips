# Generate the database dump with the following command:
#     mysqldump silverchips --xml -u root -p > /tmp/silverchips.xml

import os
from django import setup
from xml.etree import ElementTree as et
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")

setup()

from core.models import Category, Story

Category.objects.all().delete()
Story.objects.all().delete()

with open("silverchips.xml", 'r', encoding="latin-1", errors="replace") as xml_file:
    xml_data = xml_file.read()

# Eliminate special characters (except the newline)
for x in range(32):
    if x != 10:
        xml_data = xml_data.replace(chr(x), "")

# Fix quotes
xml_data = xml_data.replace(chr(146), "'")
xml_data = xml_data.replace(chr(147), "\"")
xml_data = xml_data.replace("&amp;#34;", "\"")

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

categories = read_table("category")

for old_category in categories:
    parent_id = int(get_field(old_category, "pid"))
    category = Category(id=get_field(old_category, "id"),
                        parent=(Category.objects.get(id=parent_id) if parent_id > 0 else None),
                        name=get_field(old_category, "url_name"),
                        title=get_field(old_category, "name"))
    category.save()

stories = read_table("story")

for i, old_story in enumerate(stories):
    category_id = int(get_field(old_story, "cid"))
    date = read_date(get_field(old_story, "date"))
    print("Reading story {}/{}".format(i, len(stories)))
    story = Story(id=get_field(old_story, "sid"),
                  title=get_field(old_story, "headline", "(no title)"),
                  description=get_field(old_story, "secdeck", "(no description)"),
                  lead=get_field(old_story, "lead", "(no lead)"),
                  content=get_field(old_story, "text", "(no content)"),
                  category=(Category.objects.get(id=category_id) if category_id > 0 else None),
                  created=date,
                  modified=date)
    story.save()
