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
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

# Local imports
from core import models
from core.permissions import can, VISIBILITY_ACTIONS, UserCanMixin, user_can
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

            # TODO: make this accessible

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


class ContentListView(LoginRequiredMixin, ListView):
    """The content list view that supports pagination."""

    template_name = "staff/content/list.html"
    context_object_name = "content_list"
    paginate_by = 25

    def get_queryset(self):
        """Return a list of all the content we're looking at, filtered by search criteria."""
        if self.request.user.has_perm('core.read_content'):
            content = models.Content.objects.all()
        else:
            content = models.Content.objects.filter(authors=self.request.user).all()

        form = forms.ContentSearchForm(self.request.GET)

        if form.is_valid():
            # Filter the content by certain criteria
            query = Q()

            if 'title' in form.data and form.data['title']:
                query &= Q(title__contains=form.data['title'])
            if 'id' in form.data and form.data['id']:
                query &= Q(pk=int(form.data['id']))
            if 'after' in form.data and form.data['after']:
                query &= Q(created__gt=form.data['after'])
            if 'before' in form.data and form.data['before']:
                query &= Q(created__lt=form.data['before'])
            if 'authors' in form.data and form.data['authors']:
                query &= Q(authors=form.data['authors'])

            content = content.filter(query)

        return content.order_by('-modified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ContentSearchForm(self.request.GET)
        return context


class ContentChangeMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse("staff:content:list")

    def form_valid(self, form):
        form.instance.modified = timezone.now()
        return super(ContentChangeMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = "Content"
        return context


class ContentCreateView(ContentChangeMixin, PermissionRequiredMixin, CreateView):
    """Base view for uploading new content."""

    permission = 'core.create_content'

    def get_initial(self):
        return dict(super(ContentCreateView, self).get_initial(), authors=[self.request.user])


class StoryCreateView(ContentCreateView):
    """View for uploading a new story."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/edit.html"


class ImageCreateView(ContentCreateView):
    """View for uploading a new image."""

    model = models.Image
    form_class = forms.ImageForm
    template_name = "staff/edit.html"


class ContentEditView(ContentChangeMixin, UserCanMixin, UpdateView):
    """Base view for editing content."""

    action = 'content.edit'

    def get_object(self, **kwargs):
        obj = super(ContentEditView, self).get_object(**kwargs)
        if not can(self.request.user, 'content.edit', obj):
            raise PermissionDenied
        return obj


class StoryEditView(ContentEditView):
    """View for editing stories."""

    model = models.Story
    form_class = forms.StoryForm
    template_name = "staff/edit.html"


class ImageEditView(ContentEditView):
    """View for editing images."""

    model = models.Image
    form_class = forms.ImageForm
    template_name = "staff/edit.html"


def content_edit_view(request, pk):
    content = get_object_or_404(models.Content.objects, pk=pk)

    # Switch which view gets received based on the kind of content
    return {
        'Story': StoryEditView,
        'Image': ImageEditView,
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
@user_can('content.delete')
@require_http_methods(["DELETE"])
def delete_content(request, pk):
    content = get_object_or_404(models.Content.objects, pk=pk)
    content.delete()

    return HttpResponse(status=200)


# TODO: implement this
class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Base view for creating users."""

    permission_required = 'auth.manage_users'

    model = models.User
    form_class = forms.UserForm
    template_name = "staff/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = "User"
        return context


class UserManageView(LoginRequiredMixin, UserCanMixin, UpdateView):
    """Base view for editing users."""

    action = 'users.manage'

    model = models.User
    form_class = forms.UserForm
    template_name = "staff/edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = "User"
        return context


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """The content list view that supports pagination."""

    permission_required = 'auth.manage_users'

    template_name = "staff/users/list.html"
    context_object_name = "user_list"
    paginate_by = 25

    def get_queryset(self):
        """Return a list of all the users we're looking at, filtered by search criteria."""
        users = models.User.objects.all()

        form = forms.UserSearchForm(self.request.GET)
        if form.is_valid():
            # Filter the users by certain criteria
            query = Q()

            if 'id' in form.data and form.data['id']:
                query &= Q(pk=int(form.data['id']))
            if 'first_name' in form.data and form.data['first_name']:
                query &= Q(first_name__contains=form.data['first_name'])
            if 'last_name' in form.data and form.data['last_name']:
                query &= Q(last_name__contains=form.data['last_name'])
            if 'graduation_year' in form.data and form.data['graduation_year']:
                query &= Q(profile__graduation_year=form.data['graduation_year'])
            # if 'active' in form.data and form.data['active']:
            #     query &= Q(active=form.data['active'])

            users = users.filter(query)

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.UserSearchForm(self.request.GET)
        return context


class ProfileEditView(LoginRequiredMixin, UserCanMixin, UpdateView):
    """Base view for editing users."""

    action = 'users.edit_profile'

    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "staff/edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = "Profile"
        return context
