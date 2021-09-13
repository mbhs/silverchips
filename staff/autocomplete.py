from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from dal import autocomplete

from core import models


class UserAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """Autocomplete for selecting other authors."""

    def get_queryset(self):
        """Get the list of users."""
        return models.User.objects.filter(
            Q(first_name__icontains=self.q)
            | Q(last_name__icontains=self.q)
            | Q(username__icontains=self.q)
        ).order_by("first_name", "last_name")


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        """Get the list of tags."""
        return models.Tag.objects.filter(name__icontains=self.q).order_by("name")


class ContentAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        if item:
            return "{}: {} ({}, #{})".format(
                item.type,
                item.title,
                item.section.title if item.section else "no section",
                item.pk,
            )
        else:
            return ""

    def get_queryset(self):
        """Get the list of tags."""
        return models.Content.objects.filter(
            Q(title__icontains=self.q)
            | Q(authors__first_name__icontains=self.q)
            | Q(authors__last_name__icontains=self.q)
            | Q(pk=self.q if self.q.isdigit() else None)
        ).order_by("-modified")


class SectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        if item:
            if item.parent:
                return "{} (in {})".format(item.title, item.parent.title)
            else:
                return item.title
        else:
            return ""

    def get_queryset(self):
        """Get the list of tags."""
        return models.Section.objects.filter(title__icontains=self.q).order_by("pk")
