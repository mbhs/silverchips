# Generated by Django 2.2.7 on 2020-03-04 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_search"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="linked",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="linked_content",
                to="core.Content",
            ),
        ),
        migrations.AlterField(
            model_name="galleryentrylink",
            name="order",
            field=models.PositiveIntegerField(
                db_index=True, editable=False, verbose_name="order"
            ),
        ),
    ]
