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
from core.models import Comment
from core.permissions import can, user_can
from core.decorators import check_recaptcha

from django.utils import timezone

from home.templatetags.home import render_content
from home import forms

from django.db.models import Q, Value, IntegerField

from collections import OrderedDict 

def load_context(request):
    section_roots = models.Section.objects.filter(parent=None, visible=True),  # For navigation bar
    breaking = models.Breaking.objects.all().order_by("-pk")
    sections = OrderedDict()
    for section in section_roots[0]:
        sections[section] = section.subsections.filter(visible=True)
    return {
        "section_roots": section_roots[0],
        "sections": sections,
        "breaking": breaking,
        "now": timezone.now(),  # For navigation bar
        "top_content": models.Content.objects.filter(visibility=models.Content.PUBLISHED, embed_only=False, not_instance_of=models.Image),  # For sidebar
    }


def index(request):
    """Render the index page of the Silver Chips site."""
    return render(request, "home/index.html", {
        "dense_sections": models.Section.objects.filter(index_display=models.Section.DENSE),
        "compact_sections": models.Section.objects.filter(index_display=models.Section.COMPACT),
        "list_sections": models.Section.objects.filter(index_display=models.Section.LIST),
        "feature_sections": models.Section.objects.filter(index_display=models.Section.FEATURES),
        "main_sections": models.Section.objects.filter(index_display=models.Section.MAIN)
    })


STORY_COUNT = 3


# def view_section(request, name):
#     """Render a section of the newspaper."""
#     section = get_object_or_404(models.Section, name=name)
    
#     # First load the top stories in the entire section, and then in each subsection
#     subsections = [(section, section.all_content())]
#     for subsection in section.subsections.filter(visible=True):
#         subsections.append((subsection, subsection.all_content()))

#     return render(request, "home/section.html", {
#         "section": section,
#         "subsections": subssections
#     })

class ContentList(ListView):
    """The content list view that supports pagination."""
    template_name = "home/section.html"
    context_object_name = "content_list"
    paginate_by = 25

    def get_queryset(self):
        section = get_object_or_404(models.Section, name=self.kwargs["name"])
        """Return a list of all the tags we're looking at, filtered by search criteria."""
        return section.all_content()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = self.kwargs["name"].replace("/", " » ")
        return context


@user_can('content.read')
def preview_content(request, pk):
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

    linked_content = content.linked.annotate(qs_order=Value(0, IntegerField()))

    tags = content.tags.all()
    if len(tags) > 0:
        tag_content = (models.Content.objects.filter(tags__name=tags[0].name)
                       .exclude(pk=content.pk)
                       .order_by('-modified')[:8]
                       .annotate(qs_order=Value(1, IntegerField())))
        for each_tag in tags[1:]:
            if len(tag_content) < 9:
                new_tag_content = (models.Content.objects
                                  .filter(tags__name=each_tag.name, visibility=models.Content.PUBLISHED)
                                  .exclude(pk=content.pk)
                                  .order_by('-modified')[:9-len(tag_content)]
                                  .annotate(qs_order=Value(1, IntegerField())))
                tag_content = tag_content.union(new_tag_content)

        related_content = linked_content.union(tag_content).order_by('qs_order', '-modified')
    else:
        related_content = linked_content

    return render(request, "home/content.html", {
        "content": content,
        "form": forms.CommentForm(),
        "related_content": related_content
    })


def view_profile(request, pk):
    """Render the profile of a given staff member."""
    user = get_object_or_404(models.User, id=pk)

    # Find all the content that this user authored
    stories = models.Story.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    images = models.Image.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    videos = models.Video.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    audios = models.Audio.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)
    galleries = models.Gallery.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED, embed_only=False)

    return render(request, "home/profile.html", {
        "user": user,
        "stories": stories,
        "images": images,
        "videos": videos,
        "audios": audios,
        "galleries": galleries
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

class SearchListView(ListView):
    """The content list view that supports pagination."""
    template_name = "home/search.html"
    context_object_name = "content_list"
    paginate_by = 25
    

    def get_queryset(self):
        """Return a list of all the content we're looking at, filtered by search criteria."""
        content = models.Content
        tags = models.Tag

        content_query = Q(title__icontains=self.request.GET.get('q'))
        users_query = Q(first_name__iexact=self.request.GET.get('q')) | Q(last_name__iexact=self.request.GET.get('q'))
        users = list(models.User.objects.filter(users_query).values_list('pk', flat=True))

        if users is not None:
            content_query |= Q(authors__in=users)
        return content.objects.filter(content_query, visibility=models.Content.PUBLISHED, embed_only=False, not_instance_of=models.Image).order_by('-modified')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context

def about(request):
    """Render the about page for the newspaper."""
    eics = User.objects.filter(groups__name="editors-in-chief", is_active=True)
    return render(request, "home/about/about.html", {
        "eics": eics,
    })


def staff(request):
    """Display a list of all of the newspaper's staff."""
    active_eic = User.objects.filter(groups__name="editors-in-chief", is_active=True)
    active_editor = User.objects.filter(groups__name="editors", is_active=True).exclude(groups__name="editors-in-chief")
    active_other = User.objects.filter(is_active=True).exclude(groups__name="editors-in-chief").exclude(groups__name="editors")
    inactive_users = User.objects.filter(is_active=False)
    return render(request, "home/about/staff.html", {
        "active_eic": active_eic,
        "active_editor": active_editor,
        "active_other": active_other,
        "inactive_users": inactive_users
    })


# Content interaction views
def vote(request, pk):
    """Vote in a poll."""
    pass

@check_recaptcha
def comment(request, pk):
    """Comment on a piece of content."""
    content = get_object_or_404(models.Content.objects, pk=pk)
    form = forms.CommentForm(request.POST)

    if form.is_valid() and request.recaptcha_is_valid:
        comment = form.save(commit=False)
        comment.content = content
        comment.save()
        return redirect("home:view_content", pk)
    else:
        return render(request, "home/content.html", {'content': content, 'form': form})


def carousel(request):
    stories = models.Story.objects.filter(visibility=models.Content.PUBLISHED).exclude(cover=None).order_by("pk")[:4]
    return render(request, "home/mbhs_carousel.html", {
        "stories": stories
    })

