"""Staff dashboard URL Configuration.

Included directly under /staff. Currently, the index view redirects
manually to the dashboard view.
"""


# Django imports
from django.urls import path

# Local imports
from . import views


app_name = "staff"
# Custom URL patterns
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.dummy, name="profile"),
    path("story/create/", views.create_story, name="story_create"),
    path("story/edit/<int:pk>/", views.edit_story, name="story_edit"),
    path("upload/image/", views.upload_image, name="image_upload")
]
