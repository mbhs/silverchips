from django.shortcuts import render

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework import viewsets
from core.models import *
from .serializers import ProjectPolymorphicSerializer


class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ProjectPolymorphicSerializer

class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ProjectPolymorphicSerializer
