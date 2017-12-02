"""Staff dashboard URL Configuration.

Included directly under /staff. Currently, the index view redirects
manually to the dashboard view.
"""


# Django imports
from django.conf.urls import url

# Local imports
from . import views


# Custom URL patterns
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^story/create/$", views.create_story, name="story_create"),
    url(r"^story/edit/([0-9])+/$", views.edit_story, name="story_edit"),
    url(r"^upload/image/$", views.upload_image, name="image_upload")
]
