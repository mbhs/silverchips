from rest_framework import serializers

from core.models import *

from rest_polymorphic.serializers import PolymorphicSerializer

# , Image, Video, Audio, Story, Gallery


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Content
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class ContentPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Content: ContentSerializer,
        Story: StorySerializer
    }