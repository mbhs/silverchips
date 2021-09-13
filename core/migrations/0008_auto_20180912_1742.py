# Generated by Django 2.1 on 2018-09-12 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_auto_20180912_0147"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="content",
            options={
                "ordering": ["-created"],
                "permissions": (
                    ("draft_content", "Can draft content"),
                    ("edit_content", "Can edit content"),
                    ("read_content", "Can read all content"),
                    ("publish_content", "Can publish content"),
                    ("hide_content", "Can hide content"),
                    ("create_content", "Can create content"),
                    ("editown_content", "Can edit self-authored content"),
                    ("comment", "Can manage comments"),
                ),
            },
        ),
    ]
