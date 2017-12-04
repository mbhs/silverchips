"""News home URL Configuration.

Included directly under the root of the site.
"""

# Django imports
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

# Local imports
from . import views

app_name = "home"
# Custom URL patterns
urlpatterns = [
    path("", views.index, name="index"),
    path("story/<int:pk>", views.read_story, name="read_story"),
    path("image/<int:pk>", views.view_image, name="view_image"),
    path("section/<path:name>", views.view_section, name="view_section")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
