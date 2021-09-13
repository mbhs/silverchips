from django.shortcuts import render

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework import viewsets
from core.models import *
from .serializers import *
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters


class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.filter(
        visibility=Content.PUBLISHED, embed_only=False, not_instance_of=Image
    )
    filterset_fields = ["section", "tags", "authors"]
    serializer_class = ContentPolymorphicSerializer


class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Story.objects.filter(visibility=Content.PUBLISHED, embed_only=False)
    filterset_fields = ["section", "tags", "authors"]
    serializer_class = ContentPolymorphicSerializer


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.filter(visibility=Content.PUBLISHED)
    filterset_fields = ["section", "tags", "authors"]
    serializer_class = ContentPolymorphicSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ContentPolymorphicSerializer
