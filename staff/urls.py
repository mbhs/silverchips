"""Staff dashboard URL Configuration.

Included directly under /staff. Currently, the index view redirects
manually to the dashboard view.
"""


# Django imports
from django.conf.urls import url, include

# Local imports
from . import views


# Custom URL patterns
story_urlpatterns = [
    url("^$", views.stories_view, name="view"),
    url("^edit/$", views.stories_create, name="create"),
    url("^edit/([0-9])+/$", views.stories_edit, name="edit"),
]

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^profile/$", views.dummy, name="profile"),
    url(r"^stories/", include(story_urlpatterns, namespace="stories")),
    url(r"^media/upload/$", views.upload_image, name="image_upload")
]
