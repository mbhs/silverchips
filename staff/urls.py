"""Staff dashboard URL Configuration.

Included directly under /staff. Currently, the index view redirects
manually to the dashboard view.
"""


# Django imports
from django.conf.urls import url, include

# Local imports
from . import views
from . import autocomplete


# Custom URL patterns
story_urlpatterns = [
    url("^$", views.stories_view, name="view"),
    url("^edit/$", views.stories_create, name="create"),
    url("^edit/([0-9])+/$", views.stories_edit, name="edit"),
]

autocomplete_urlpatterns = [
    url("^users/$", autocomplete.UserAutoComplete.as_view(), name="users"),
]

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^login/$", views.login, name="login"),
    url("^logout/$", views.logout, name="logout"),
    url("^profile/$", views.dummy, name="profile"),
    url("^stories/", include(story_urlpatterns, namespace="stories")),
    url("^media/upload/$", views.upload_image, name="image_upload"),
    url("^autocomplete/", include(autocomplete_urlpatterns, namespace="autocomplete"))
]
