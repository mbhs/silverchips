"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""

# Django imports
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User

# News imports
from core import models
from core.permissions import can, user_can
from home import forms

from django.utils import timezone

from home.templatetags.home import render_content


def load_context(request):
    return {
        "section_roots": models.Section.objects.filter(parent=None),  # For navigation bar
        "now": timezone.now(),  # For navigation bar
        "stories": models.Story.objects.filter(visibility=models.Content.PUBLISHED, embed_only=False)  # For sidebar
    }


def index(request):
    """Render the index page of the SilverChips site."""
    return render(request, "home/index.html")


STORY_COUNT = 3


def view_section(request, name):
    """Render a section of the newspaper."""
    section = get_object_or_404(models.Section, name=name)

    # Get the top STORY_COUNT stories in the section
    top_stories = section.all_stories()[:STORY_COUNT]
    subsections = [(None, top_stories)]

    for subsection in section.subsections.all():
        subsections.append((subsection,
                            subsection.all_stories().filter(visibility=models.Content.PUBLISHED)
                            .exclude(id__in=top_stories.values_list('id', flat=True))))  # Exclude our top stories

    return render(request, "home/section.html", {
        "section": section,
        "subsections": subsections
    })


@user_can('content.read')
def embed_content(request, pk, slug=None):
    """Render specific content in the newspaper."""
    content = get_object_or_404(models.Content, pk=pk)
    return HttpResponse(render_content(request.user, content))


@user_can('content.read')
def view_content(request, pk, slug=None):
    """Render specific content in the newspaper."""
    content = get_object_or_404(models.Content, pk=pk)

    # Redirect to the correct URL for the content
    # We allow accessing with any slug, but redirect to the correct slug
    if content.slug != slug:
        return redirect("home:view_content", content.slug, content.pk)

    if content.embed_only and not can(request.user, 'content.edit', content):
        # This content shouldn't have it's own page!
        return HttpResponseForbidden("This content is for embedding only.")

    # Mark another view for the content
    content.views += 1
    content.save()

    return render(request, "home/content.html", {
        "content": content
    })


def view_profile(request, pk):
    """Render the profile of a given staff member."""
    user = get_object_or_404(models.User, id=pk)

    # Find all the content that this user authored
    stories = models.Story.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    images = models.Image.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    videos = models.Video.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    audios = models.Audio.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)

    return render(request, "home/profile.html", {
        "user": user,
        "stories": stories,
        "images": images,
        "videos": videos,
        "audios": audios
    })


def legacy(klass):
    """A function that, given a content class, constructs a view which redirects legacy URLs to their current homes."""
    def legacy_view(request, pk):
        content = get_object_or_404(klass, legacy_id=pk)
        return redirect('home:view_content', content.pk)
    return legacy_view


class TaggedContentList(ListView):
    """The content list view that supports pagination."""
    template_name = "home/tag.html"
    context_object_name = "content_list"
    paginate_by = 25

    def get_queryset(self):
        """Return a list of all the tags we're looking at, filtered by search criteria."""
        return models.Content.objects.filter(tags__name=self.kwargs["tag"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs["tag"]
        return context


def about(request):
    """Render the about page for the newspaper."""
    eics = User.objects.filter(groups__name="editors-in-chief")
    return render(request, "home/about/about.html", {
        "eics": eics,
    })


def staff(request):
    """Display a list of all of the newspaper's staff."""
    active_users = User.objects.filter(is_active=True).order_by('profile__graduation_year')
    inactive_users = User.objects.filter(is_active=False).order_by('profile__graduation_year')
    return render(request, "home/about/staff.html", {
        "active_users": active_users,
        "inactive_users": inactive_users
    })


# Content interaction views
def vote(request):
    """Vote in a poll."""
    pass  # STUB_POLL


class CommentSubmitView(CreateView):
    pass  # STUB_COMMENT
