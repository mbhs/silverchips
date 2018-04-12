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

create_urlpatterns = ([
    path("story/", views.StoryCreateView.as_view(), name="story")
], "create")

content_urlpatterns = ([
    path("list/", views.ContentListView.as_view(), name="list"),
    path("edit/<int:pk>/", views.content_edit_view, name="edit"),
    path("create/", include(create_urlpatterns, "create"))
], "content")

autocomplete_urlpatterns = ([
    path("users/", autocomplete.UserAutoComplete.as_view(), name="users"),
], "autocomplete")

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("content/", include(content_urlpatterns, "content")),
    path("autocomplete/", include(autocomplete_urlpatterns, "autocomplete"))
]
