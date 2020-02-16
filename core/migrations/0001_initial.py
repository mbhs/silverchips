# Generated by Django 2.1 on 2018-08-01 18:13

import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('legacy_id', models.IntegerField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest_authors', models.CharField(blank=True, default='', max_length=64)),
                ('views', models.IntegerField(default=0)),
                ('embed_only', models.BooleanField(default=False, help_text='Whether this content should be used only in the context of embedding into other content (especially stories), or whether it should appear independently on the site. You will often mark content as embed only when it is not original or when it is meaningless outside of some broader story.')),
                ('visibility', models.IntegerField(choices=[(1, 'draft'), (2, 'pending'), (3, 'published'), (0, 'hidden')], default=1)),
            ],
            options={
                'permissions': (('draft_content', 'Can draft content'), ('edit_content', 'Can edit content'), ('read_content', 'Can read all content'), ('publish_content', 'Can publish content'), ('hide_content', 'Can hide content'), ('create_content', 'Can create content')),
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='GalleryEntryLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'ordering': ('gallery', 'order'),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.TextField(help_text='A short biography, often including likes and dislikes, accomplishments, etc. Should be several sentences minimum.')),
                ('avatar', models.ImageField(null=True, upload_to='')),
                ('position', models.TextField()),
                ('graduation_year', models.IntegerField(default=2022)),
            ],
            options={
                'permissions': (('edit_profile', "Can edit one's own user profile"),),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('title', models.CharField(max_length=64)),
                ('visible', models.BooleanField(default=True)),
                ('index_display', models.IntegerField(choices=[(-1, '-1'), (0, 'dense'), (1, 'compact'), (2, 'list'), (3, 'features'), (4, 'main')], default=-1)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subsections', to='core.Section')),
            ],
            options={
                'verbose_name_plural': 'sections',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'permissions': (('manage_users', 'Can manage user data and privileges'),),
                'indexes': [],
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', core.models.ProfileUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
                ('source', models.FileField(upload_to='audio/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.content',),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.content',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
                ('source', models.ImageField(upload_to='images/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.content',),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.content',),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
                ('second_deck', models.TextField()),
                ('text', models.TextField()),
                ('cover', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Image')),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
            bases=('core.content',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Content')),
                ('source', models.FileField(upload_to='videos/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.content',),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='core.User'),
        ),
        migrations.AddField(
            model_name='galleryentrylink',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_links', to='core.Content'),
        ),
        migrations.AddField(
            model_name='content',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='content_authored', to='core.User'),
        ),
        migrations.AddField(
            model_name='content',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.content_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='content',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='core.Section'),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
        migrations.AddField(
            model_name='galleryentrylink',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_links', to='core.Gallery'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='entries',
            field=models.ManyToManyField(related_name='containing_galleries', through='core.GalleryEntryLink', to='core.Content'),
        ),
    ]
