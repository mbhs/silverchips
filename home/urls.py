"""News home URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.urls import path, include

# Local imports
from . import views

app_name = "home"


about_urlpatterns = ([
    path("", views.about, name="index"),
    path("about/", views.staff, name="staff")
], "about")

urlpatterns = [
    path("", views.index, name="index"),
    path("c/<int:pk>/", views.view_content, name="view_content"),  # Short URLs for content
    path("content/<int:pk>/", views.view_content, name="view_content"),
    path("content/<slug:slug>-<int:pk>/", views.view_content, name="view_content"),
    path("profile/<int:pk>/", views.view_profile, name="view_profile"),
    path("section/<path:name>/", views.view_section, name="view_section"),
    path("about/", include(about_urlpatterns, "about")),
    path("vote/<int:pk>/<int:choice>/", views.vote, name="vote")
]
