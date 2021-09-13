# Generated by Django 2.1 on 2018-09-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20180903_1525"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("date",)},
        ),
        migrations.AddField(
            model_name="comment",
            name="approved",
            field=models.BooleanField(default=False),
        ),
    ]
