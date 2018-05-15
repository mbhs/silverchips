from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from core.models import User


class UserAutoComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """Autocomplete for selecting other authors."""

    def get_queryset(self):
        """Get the list of users."""
        return User.objects.filter(first_name__istartswith=self.q).order_by("first_name", "last_name")
