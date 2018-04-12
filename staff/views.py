"""The staff view map.

Handles the side of the site for writers, editors, and managers.
Also allows for some degree of customization.
"""


# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

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
    """Return the staff dashboard page."""

    return render(request, "staff/index.html")


class ContentListView(ListView):
    """The content list view that supports pagination."""

    template_name = "staff/content/list.html"
    context_object_name = "content_list"
    paginate_by = 25

    def get_queryset(self):
        """Get all stories by the request user."""

        return models.Content.objects.filter(authors=self.request.user).all()


class ContentChangeMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse("staff:content:list")


class ContentCreateView(ContentChangeMixin, CreateView):
    """Base view for uploading new content."""

    def get_initial(self):
        return dict(super(ContentCreateView, self).get_initial(), authors=[self.request.user])


class StoryCreateView(ContentCreateView):
    """View for uploading a new story."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/content/edit.html"


class ImageCreateView(ContentCreateView):
    """View for uploading a new image."""

    model = models.Image
    form_class = forms.ImageForm
    template_name = "staff/content/edit.html"


class ContentEditView(ContentChangeMixin, UpdateView):
    """Base view for editing content."""

    pass


class StoryEditView(ContentEditView):
    """View for editing stories."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/content/edit.html"


def content_edit_view(request, pk):
    content = get_object_or_404(models.Content.objects, pk=pk)

    # Switch which view gets received based on the kind of content
    return {
        models.Story: StoryEditView
    }[type(content)].as_view()(request, pk=pk)
