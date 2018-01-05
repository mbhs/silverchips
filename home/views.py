"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""

# Django imports
from django.shortcuts import render, get_object_or_404, redirect

# News imports
from core.models import Story, Image, Video, Audio, Section, User, Comment
from . import forms

def load_context(request):
    return {
        "section_roots": Section.objects.filter(parent=None),
        "stories": Story.objects.all()
    }


def index(request):
    """Return the index page of the Silver Chips site."""

    return render(request, "home/index.html")


SECTION_COUNT = 5

def view_section(request, name):
    """Render a section of the newspaper."""

    section = get_object_or_404(Section, name=name)

    top_stories = section.all_stories().all()[:SECTION_COUNT]
    subsections = [(None, top_stories)]

    for subsection in section.subsections.all():
        subsections.append((subsection,
                            subsection.all_stories().exclude(id__in=top_stories.values_list('id', flat=True))))

    print(subsections)

    return render(request, "home/section.html", {
        "section": section,
        "subsections": subsections
    })


def read_story(request, pk):
    """Render a specific newspaper story."""

    story = get_object_or_404(Story, id=int(pk))

    story.views += 1
    story.save()

    return render(request, "home/story.html", {
        "story": story,
        "authorized_comments": story.get_authorized_comments(),
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

# voting url routing broken, probably add captcha
def updoot(request, comment_pk, story_pk):
    """Updoots a post"""

    story = get_object_or_404(Story, id=int(story_pk))

    if story.comments_on:
        comment = get_object_or_404(Comment, id=int(comment_pk))
        comment.rating += 1
        comment.save()
    return redirect('/story/' + str(story_pk))

def post_comment(request, story_pk):
    """Posts a comment"""

    # Check if post and validate
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():

            story = get_object_or_404(Story, id=int(story_pk))

            if story.comments_on:
                # Get name and text
                name = form.cleaned_data["name"]
                text = form.cleaned_data["text"]

                # save comment
                comment = Comment(name=name, text=text)
                comment.save()

                story.comments.add(comment)
                story.save()

        else:
            form = forms.CommentForm()

    else:
        form = forms.CommentForm()

    return redirect('/story/' + str(story_pk))

def post_reply(request, story_pk, parent_pk):
    """Posts a reply"""

    # Check if post and validate
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():

            story = get_object_or_404(Story, id=int(story_pk))

            if story.comments_on:
                # Get name and text
                name = form.cleaned_data["name"]
                text = form.cleaned_data["text"]

                # save comment
                comment = Comment(name=name, text=text)
                comment.save()

                parent = get_object_or_404(Comment, id=int(parent_pk))
                parent.replies.add(comment)
                parent.save()

        else:
            form = forms.CommentForm()

    else:
        form = forms.CommentForm()

    return redirect('/story/' + str(story_pk))

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
