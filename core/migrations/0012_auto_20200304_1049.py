# Generated by Django 2.1.2 on 2020-03-04 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_auto_20200304_0947"),
    ]

    operations = [
        migrations.AlterField(
            model_name="galleryentrylink",
            name="order",
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
    ]
