"""Staff dashboard URL Configuration.

Included directly under /staff. Currently, the index view redirects
manually to the dashboard view.
"""


# Django imports
from django.urls import path, include

# Local imports
from . import views
from . import autocomplete


app_name = "staff"
# Custom URL patterns
story_urlpatterns = [
    path("", views.stories_view, name="view"),
    path("edit/", views.stories_create, name="create"),
    path("edit/<int:pk>/", views.stories_edit, name="edit"),
]

autocomplete_urlpatterns = [
    path("users/", autocomplete.UserAutoComplete.as_view(), name="users"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.dummy, name="profile"),
    path("upload/image/", views.upload_image, name="image_upload"),
    path("media/upload/", views.upload_image, name="image_upload"),
    path("stories/", include((story_urlpatterns, "story"))),
    path("autocomplete/", include((autocomplete_urlpatterns, "autocomplete")))
]
