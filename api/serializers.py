from rest_framework import serializers

from core.models import *

from rest_polymorphic.serializers import PolymorphicSerializer

# , Image, Video, Audio, Story, Gallery


class TagSerializer(serializers.HyperlinkedReadOnlyModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'name')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = ('url', 'name')


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    # tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Content
        fields = ('url', 'title', 'description', 'tags', 'legacy_id', 'created', 'modified',
                  'authors', 'guest_authors', 'section', 'views', 'embed_only', 'linked')


class StorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        fields = ('url', 'title', 'description', 'tags', 'legacy_id', 'created', 'modified',
                  'authors', 'guest_authors', 'section', 'views', 'embed_only', 'linked',
                  'second_deck', 'text', 'cover', 'template', 'descriptor', 'hide_caption')


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Content: ContentSerializer,
        Story: StorySerializer
    }