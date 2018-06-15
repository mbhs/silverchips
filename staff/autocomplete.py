from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from dal import autocomplete

from core.models import User, Tag


class UserAutoComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """Autocomplete for selecting other authors."""

    def get_queryset(self):
        """Get the list of users."""
        return User.objects.filter(Q(first_name__icontains=self.q) |
                                   Q(last_name__icontains=self.q) |
                                   Q(username__icontains=self.q)).order_by("first_name", "last_name")


class TagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        """Get the list of tags."""
        return Tag.objects.filter(Q(name__icontains=self.q)).order_by("name")

Tag.objects.all().delete()
for t in ['opinions', 'news', 'lifestyle', 'sports', 'spanish', 'blogs']:
    tag = Tag(name=t)
    tag.save()
