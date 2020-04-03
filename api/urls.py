"""API URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from api import views


router = DefaultRouter()
router.register(r'content', views.ContentViewSet)
router.register(r'stories', views.StoryViewSet)
router.register(r'tags', views.TagViewSet)


urlpatterns = [
    path("", include(router.urls))
]
