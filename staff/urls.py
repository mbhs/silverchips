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
    path("story/", views.StoryCreateView.as_view(), name="story"),
    path("image/", views.ImageCreateView.as_view(), name="image"),
    path("video/", views.VideoCreateView.as_view(), name="video"),
    path("audio/", views.AudioCreateView.as_view(), name="audio"),
    path("poll/", views.PollCreateView.as_view(), name="poll")
], "create")

content_urlpatterns = ([
    path("list/", views.ContentListView.as_view(), name="list"),
    path("visibility/set/<int:pk>/<int:level>/", views.set_content_visibility, name="set_visibility"),
    path("delete/<int:pk>/", views.delete_content, name="delete"),
    path("edit/<int:pk>/", views.content_edit_view, name="edit"),
    path("create/", include(create_urlpatterns, "create"))
], "content")

user_urlpatterns = ([
    path("manage/<int:pk>/", views.UserManageView.as_view(), name="manage"),
    path("create/", views.UserCreateView.as_view(), name="create"),
    path("self-manage/", views.UserSelfManageView.as_view(), name="self_manage"),
    path("list/", views.UserListView.as_view(), name="list")
], "users")

autocomplete_urlpatterns = ([
    path("users/", autocomplete.UserAutocomplete.as_view(), name="users"),
    path("tags/", autocomplete.TagAutocomplete.as_view(create_field="name"), name="tags")
], "autocomplete")

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("content/", include(content_urlpatterns, "content")),
    path("autocomplete/", include(autocomplete_urlpatterns, "autocomplete")),
    path("users/", include(user_urlpatterns, "user"))
]
