from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.models import *

from rest_polymorphic.serializers import PolymorphicSerializer
from django.contrib.contenttypes.models import ContentType
# , Image, Video, Audio, Story, Gallery


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'biography', 'avatar', 'position', 'graduation_year', 'user')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()
    name = serializers.CharField(source="__str__")

    class Meta:
        model = User
        fields = ('url', 'name', 'profile')

# For self-referencing objects
# https://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    subsections = RecursiveField(many=True)

    class Meta:
        model = Section
        fields = ('url', 'parent', 'title', 'subsections')

    # def get_fields(self):
    #     fields = super(SectionSerializer, self).get_fields()
    #     fields['subcategories'] = SectionSerializer(many=True)
    #     return fields
    # def get_parent(self, obj):
    #     if obj.parent is not None:
    #         return SectionSerializer(obj.parent, context=self.context).data
    #     else:
    #         return None


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()

    class Meta:
        model = Content
        fields = ('url', 'title', 'description', 'tags', 'created', 'modified',
                  'authors', 'guest_authors', 'section', 'views', 'embed_only', 'linked', 'share_url')

    def get_share_url(self, obj):
        return obj.get_absolute_url()

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    share_url = SerializerMethodField()

    class Meta:
        model = Image
        fields = ('url', 'title', 'description', 'tags', 'created', 'modified',
                  'authors', 'guest_authors', 'section', 'views', 'embed_only', 'linked', 'descriptor', 'share_url')

    def get_share_url(self, obj):
        return obj.get_absolute_url()

class StorySerializer(serializers.HyperlinkedModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()
    cover = ImageSerializer(required=False)

    class Meta:
        model = Story
        fields = ('url', 'title', 'description', 'tags', 'created', 'modified',
                  'authors', 'guest_authors', 'section', 'views', 'embed_only', 'linked',
                  'second_deck', 'text', 'cover', 'template', 'hide_caption', 'descriptor', 'share_url')

    def get_share_url(self, obj):
        return obj.get_absolute_url()


class ContentPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Content: ContentSerializer,
        Story: StorySerializer,
        Image: ImageSerializer
    }
