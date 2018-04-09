"""The staff view map.

Handles the side of the site for writers, editors, and managers.
Also allows for some degree of customization.
"""


# Django imports
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from polymorphic.contrib.extra_views import PolymorphicFormSetView
from polymorphic.formsets import PolymorphicFormSetChild

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
        form = forms.LoginForm(request.POST)
        if form.is_valid():

            # Get username, password, and corresponding User
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)

            # Check if password wrong
            if not user:
                form.add_error(None, "Invalid credentials")

            # Check if user is inactive
            elif not user.is_active:
                form.add_error(None, "User is inactive")

            # Login and redirect to staff
            else:
                auth.login(request, user)
                return redirect("staff:index")

    else:
        form = forms.LoginForm()

    return render(request, "staff/login.html", {"form": form})


@login_required
def logout(request):
    """Log out the user and go to logout page."""

    auth.logout(request)
    return redirect("/staff")


@login_required
def index(request):
    """Return the index page. Redirects to the dashboard."""

    return render(request, "staff/index.html")


@login_required
def profile(request):
    """Get the user profile page."""

    return render(request, "staff/profile.html")


@login_required
def dummy(request):
    """Dummy page generator."""

    return render(request, "staff/base.html")


class StoryListView(ListView):
    """The story list view that supports pagination."""

    model = models.Story
    template_name = "staff/story/list.html"
    context_object_name = "stories"
    paginate_by = 25

    def get_queryset(self):
        """Get all stories by the request user."""

        return models.Story.objects.filter(authors=self.request.user)


class StoryCreateView(LoginRequiredMixin, CreateView):
    """View for uploading a new story."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/story/edit.html"

    def get_success_url(self):
        return reverse("staff:stories:view")


@login_required
def stories_edit(request, story_id):
    story_id = int(story_id)
    story = models.Story.objects.get(id=story_id)

    if request.method == 'POST':
        form = forms.StoryForm(request.POST, instance=story)

        if form.is_valid():
            form.save()
            return redirect("story", story_id)
    else:
        form = forms.StoryForm(instance=story)

    return render(request, "staff/story/edit.html", {"form": form})


class ImageCreateView(CreateView):
    """View for uploading images to the staff site."""

    model = models.Image

    form_class = forms.ImageForm
    # TODO: set active user as uploader

    template_name = "staff/media/edit.html"
