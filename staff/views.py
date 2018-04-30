"""The staff view map.

Handles the side of the site for writers, editors, and managers.
Also allows for some degree of customization.
"""


# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone

# Local imports
from core import models
from core.permissions import can, VISIBILITY_ACTIONS
from staff import forms


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
    return redirect("staff:index")


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

        if self.request.user.has_perm('core.read_content'):
            return models.Content.objects.all()
        else:
            return models.Content.objects.filter(authors=self.request.user).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['pages'] = range(3)
        return context


class ContentChangeMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse("staff:content:list")

    def form_valid(self, form):
        form.instance.modified = timezone.now()
        return super(ContentChangeMixin, self).form_valid(form)


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

    def get_object(self, **kwargs):
        obj = super(ContentEditView, self).get_object(**kwargs)
        if not can(self.request.user, 'edit', obj):
            raise PermissionDenied
        return obj


class StoryEditView(ContentEditView):
    """View for editing stories."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/content/edit.html"


def content_edit_view(request, pk):
    content = get_object_or_404(models.Content.objects, pk=pk)

    # Switch which view gets received based on the kind of content
    return {
        'Story': StoryEditView
    }[content.type].as_view()(request, pk=pk)


@login_required
@csrf_protect
@require_http_methods(["PATCH"])
def set_content_visibility(request, pk, level):
    content = get_object_or_404(models.Content.objects, pk=pk)

    if not can(request.user, VISIBILITY_ACTIONS[level], content):
        raise PermissionDenied

    content.visibility = level
    content.save()

    return HttpResponse(status=200)


@login_required
@csrf_protect
@require_http_methods(["DELETE"])
def delete_content(request, pk):
    content = get_object_or_404(models.Content.objects, pk=pk)

    if not can(request.user, 'delete', content):
        raise PermissionDenied

    content.delete()

    return HttpResponse(status=200)