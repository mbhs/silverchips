# Generated by Django 3.2.7 on 2021-10-04 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_profile_is_hidden"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("priority", models.PositiveSmallIntegerField()),
                ("url", models.CharField(max_length=2048)),
                ("text", models.CharField(max_length=500)),
            ],
        ),
    ]
