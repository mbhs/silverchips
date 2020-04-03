"""API URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from api import views


router = DefaultRouter()
router.register(r'snippets', views.ContentViewSet)
router.register(r'users', views.StoryViewSet)


urlpatterns = [
    path("", include(router.urls))
]
