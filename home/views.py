"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""


# Django imports
from django.shortcuts import render

# News imports
from core.models import Story, Image

# Create your views here
def index(request):
    """Return the index page of the Silver Chips site."""
    return render(request, "home/index.html")

def story(request, story_id):
    """Render a specific newspaper story."""
    
    story_id = int(story_id)
    
    return render(request, "home/story.html", {"story": Story.objects.get(id=story_id)})

def image(request, image_id):
    """Render a specific newspaper story."""

    story_id = int(image_id)

    return render(request, "home/image.html", {"image": Image.objects.get(id=image_id)})