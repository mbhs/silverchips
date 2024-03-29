from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.models import *

from rest_polymorphic.serializers import PolymorphicSerializer
from django.contrib.contenttypes.models import ContentType

# , Image, Video, Audio, Story, Gallery


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "biography", "avatar", "position", "graduation_year", "user")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    name = serializers.CharField(source="__str__")

    class Meta:
        model = User
        fields = ("id", "name", "profile")


# For self-referencing objects
# https://stackoverflow.com/questions/13376894/django-rest-framework-nested-self-referential-objects
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SectionSerializer(serializers.ModelSerializer):
    subsections = RecursiveField(many=True)

    class Meta:
        model = Section
        fields = ("id", "parent", "title", "subsections")


class ContentSerializer(serializers.ModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()

    class Meta:
        model = Content
        fields = (
            "id",
            "title",
            "description",
            "tags",
            "created",
            "modified",
            "authors",
            "guest_authors",
            "section",
            "views",
            "embed_only",
            "linked",
            "share_url",
        )

    def get_share_url(self, obj):
        return obj.get_absolute_url()


class ImageSerializer(serializers.ModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()

    class Meta:
        model = Image
        fields = (
            "id",
            "title",
            "description",
            "tags",
            "created",
            "modified",
            "authors",
            "guest_authors",
            "section",
            "views",
            "embed_only",
            "linked",
            "descriptor",
            "share_url",
        )

    def get_share_url(self, obj):
        return obj.get_absolute_url()


class GallerySerializer(serializers.ModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()

    class Meta:
        model = Image
        fields = (
            "id",
            "title",
            "description",
            "tags",
            "created",
            "modified",
            "authors",
            "guest_authors",
            "section",
            "views",
            "embed_only",
            "linked",
            "descriptor",
            "share_url",
        )

    def get_share_url(self, obj):
        return obj.get_absolute_url()


class StorySerializer(serializers.ModelSerializer):
    section = SectionSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    authors = UserSerializer(required=False, many=True)
    share_url = SerializerMethodField()
    cover = ImageSerializer(required=False)

    class Meta:
        model = Story
        fields = (
            "id",
            "title",
            "description",
            "tags",
            "created",
            "modified",
            "authors",
            "guest_authors",
            "section",
            "views",
            "embed_only",
            "linked",
            "second_deck",
            "text",
            "cover",
            "descriptor",
            "share_url",
        )

    def get_share_url(self, obj):
        return obj.get_absolute_url()


class ContentPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Content: ContentSerializer,
        Story: StorySerializer,
        Image: ImageSerializer,
        Gallery: GallerySerializer,
    }
