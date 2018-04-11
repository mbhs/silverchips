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

content_urlpatterns = ([
    path("user", views.ContentListView.as_view(), name="list"),
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
