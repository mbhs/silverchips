"""News home URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

# Local imports
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("story/<int:pk>", views.read_story, name="read_story"),
    path("image/<int:pk>", views.view_image, name="view_image"),
    path("video/<int:pk>", views.view_video, name="view_video"),
    path("audio/<int:pk>", views.view_video, name="view_audio"),
    path("profile/<int:pk>", views.view_profile, name="view_profile"),
    path("section/<path:name>", views.view_section, name="view_section"),
    path("vote/<int:comment_pk>/<int:story_pk>", views.updoot, name="updoot"),
    path("comment/<int:story_pk>", views.post_comment, name="post_comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
