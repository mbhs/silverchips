"""News home URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.urls import path, include

# Local imports
from home import views
from core import models

app_name = "home"


about_urlpatterns = ([
    path("", views.about, name="index"),
    path("staff/", views.staff, name="staff")
], "about")

urlpatterns = [
    path("", views.index, name="index"),

    path("c/<int:pk>/", views.view_content, name="view_content"),  # Short URLs for content
    path("content/<int:pk>/", views.view_content, name="view_content"),
    path("content/<slug:slug>-<int:pk>/", views.view_content, name="view_content"),
    path("content/preview/<int:pk>/", views.preview_content, name="embed_content"),
    path("tagged/<path:tag>/", views.TaggedContentList.as_view(), name="tagged"),  # path guarantees we can have tags with slashes

    path("profile/<int:pk>/", views.view_profile, name="view_profile"),
    path("section/<path:name>/all/", views.all_section, name="all_section"),
    path("section/<path:name>/", views.view_section, name="view_section"),
    path("about/", include(about_urlpatterns, "about")),

    path("vote/<int:pk>/<int:choice>/", views.vote, name="vote"),
    path("comment/submit/<int:pk>/", views.comment, name="submit_comment"),

    # Legacy URLs to make sure old links work
    path("story/<int:pk>/", views.legacy(models.Story)),
    path("picture/<int:pk>/", views.legacy(models.Image)),

    # mbhs.edu homepage needs carousel query
    path("carousel/", views.carousel, name="carousel")
]
