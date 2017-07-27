"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""


# Django imports
from django.shortcuts import render, get_object_or_404

# News imports
from core.models import Story, Image, Category


# Create your views here
def index(request):
    """Return the index page of the Silver Chips site."""

    roots = Category.objects.filter(parent=None)

    return render(request, "home/index.html", {
        "roots": roots
    })


def read_story(request, story_id):
    """Render a specific newspaper story."""

    story = get_object_or_404(Story, id=int(story_id))

    story.views += 1
    story.save()
    
    return render(request, "home/story.html", {
        "story": story,
        "stories": Story.objects.all()
    })


def view_image(request, image_id):
    """Render a specific newspaper image."""

    image = get_object_or_404(Image, id=int(image_id))

    return render(request, "home/story.html", {
        "story": image,
        "stories": Story.objects.all()
    })