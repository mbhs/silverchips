"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""

# Django imports
from django.shortcuts import render, get_object_or_404

# News imports
from core.models import Story, Image, Video, Audio, Section, User


def load_context(request):
    return {
        "section_roots": Section.objects.all(),
        "stories": Story.objects.all()
    }


def index(request):
    """Return the index page of the Silver Chips site."""

    return render(request, "home/index.html")


def view_section(request, name):
    """Render a section of the newspaper."""

    section = get_object_or_404(Section, name=name)

    return render(request, "home/section.html", {
        "section": section
    })


def read_story(request, pk):
    """Render a specific newspaper story."""

    story = get_object_or_404(Story, id=int(pk))

    story.views += 1
    story.save()

    return render(request, "home/story.html", {
        "story": story
    })

def view_image(request, pk):
    """Render a specific newspaper image."""

    image = get_object_or_404(Image, id=int(pk))

    return render(request, "home/story.html", {
        "story": image
    })

def view_video(request, pk):
    """Render video."""

    video = get_object_or_404(Video, id=int(pk))

    return render(request, "home/story.html", {
        "story": video,
        "stories": Story.objects.all()
    })

def view_audio(request, pk):
    """Render audio."""

    audio = get_object_or_404(Audio, id=int(pk))

    return render(request, "home/story.html", {
        "story": audio,
        "stories": Story.objects.all()
    })

def post_comment(request, pk):
    

def view_profile(request, pk):
    """Render the profile of a given staff member."""

    user = get_object_or_404(User, id=int(pk))

    # Find all the content that this user authored
    stories = Story.objects.filter(authors__in=[user])
    photos = Image.objects.filter(authors__in=[user])

    return render(request, "home/profile.html", {
        "user": user,
        "stories": stories,
        "photos": photos
    })
