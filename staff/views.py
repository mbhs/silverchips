"""The staff view map.

Handles the side of the site for writers, editors, and managers.
Also allows for some degree of customization.
"""


# Django imports
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import ModelFormMixin

# Local imports
from . import forms
from core import models


# The main views
def login(request):
    """Return the login page to the staff site."""

    if request.user.is_authenticated:
        return redirect("staff:index")

    # Check if post and validate
    if request.method == "POST":
        form = forms.Login(request.POST)
        if form.is_valid():

            # Get username, password, and corresponding User
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)

            # Check if password wrong
            if user is False:
                return redirect("/staff/login?error=1")

            # Check if no user
            if user is None:
                return redirect("/staff/login?error=2")

            # Check if user is inactive
            if not user.is_active:
                return redirect("/staff/login?error=3")

            # Login and redirect to staff
            auth.login(request, user)
            return redirect("staff:index")

    else:
        form = forms.Login()

    return render(request, "staff/login.html", {"form": form})


@login_required
def index(request):
    """Return the index page. Redirects to the dashboard."""

    return render(request, "staff/index.html")


@login_required
def dashboard(request):
    """Return the dashboard to the staff site."""

    return render(request, "staff/index.html")


@login_required
def logout(request):
    """Log out the user and go to logout page."""

    auth.logout(request)
    return redirect("/")


@login_required
def dummy(request):
    """Dummy page generator."""

    return render(request, "staff/base.html")


@login_required
def stories_view(request):
    """View stories."""

    return render(request, "staff/base.html")


@login_required
def stories_create(request):
    if request.method == 'POST':
        form = forms.Story(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.uploader = request.user
            story.save()
            return redirect("story", story.id)
    else:
        form = forms.Story()

    return render(request, "staff/story_edit.html", {
        "form": form
    })


@login_required
def stories_edit(request, story_id):
    story_id = int(story_id)
    story = models.Story.objects.get(id=story_id)

    if request.method == 'POST':
        form = forms.Story(request.POST, instance=story)

        if form.is_valid():
            form.save()
            return redirect("story", story_id)
    else:
        form = forms.Story(instance=story)

    return render(request, "staff/story_edit.html", {
        "form": form
    })


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = forms.Image(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            print(image.get_upload_to("cooler"))

            return redirect("image", image.id)
    else:
        form = forms.Image()

    return render(request, "staff/media_upload.html", {
        "form": form
    })