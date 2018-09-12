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


gallery_urlpatterns = ([
    path("<int:pk>/insert/", views.gallery_insert, name="insert"),
    path("<int:pk>/swap/", views.gallery_swap, name="swap"),
    path("<int:pk>/remove/", views.gallery_remove, name="remove")
], "gallery")

create_urlpatterns = ([
    path("story/", views.StoryCreateView.as_view(), name="story"),
    path("gallery/", views.GalleryCreateView.as_view(), name="gallery"),
    path("image/", views.ImageCreateView.as_view(), name="image"),
    path("video/", views.VideoCreateView.as_view(), name="video"),
    path("audio/", views.AudioCreateView.as_view(), name="audio"),
    path("poll/", views.PollCreateView.as_view(), name="poll")
], "create")

content_urlpatterns = ([
    path("list/", views.ContentListView.as_view(), name="list"),
    path("<int:pk>/set-visibility/<int:level>/", views.set_content_visibility, name="set_visibility"),
    path("<int:pk>/delete/", views.delete_content, name="delete"),
    path("<int:pk>/edit/", views.content_edit_view, name="edit"),
    path("create/", include(create_urlpatterns, "create")),
    path("gallery/", include(gallery_urlpatterns, "gallery"))
], "content")

comment_urlpatterns = ([
    path("list/", views.CommentListView.as_view(), name="list"),
    path("<int:pk>/set-approval/<int:level>/", views.set_comment_approval, name="set_approval"),
    path("<int:pk>/delete/", views.delete_comment, name="delete_comment"),
], "comment")

user_urlpatterns = ([
    path("<int:pk>/manage/", views.UserManageView.as_view(), name="manage"),
    path("create/", views.UserCreateView.as_view(), name="create"),
    path("self-manage/", views.UserSelfManageView.as_view(), name="self_manage"),
    path("list/", views.UserListView.as_view(), name="list")
], "users")

autocomplete_urlpatterns = ([
    path("users/", autocomplete.UserAutocomplete.as_view(), name="users"),
    path("tags/", autocomplete.TagAutocomplete.as_view(create_field="name"), name="tags"),
    path("content/", autocomplete.ContentAutocomplete.as_view(), name="content"),
    path("section/", autocomplete.SectionAutocomplete.as_view(), name="section")
], "autocomplete")

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("content/", include(content_urlpatterns, "content")),
    path("comment/", include(comment_urlpatterns, "comment")),
    path("autocomplete/", include(autocomplete_urlpatterns, "autocomplete")),
    path("users/", include(user_urlpatterns, "user"))
]
