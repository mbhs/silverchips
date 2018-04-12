from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete
from core.models import User


class UserAutoComplete(autocomplete.Select2QuerySetView, LoginRequiredMixin):
    """Autocomplete for selecting other authors."""

    def get_queryset(self):
        """Get the list of users."""

        if not self.request.user.is_authenticated:
            return User.objects.none()

        return User.objects.filter(first_name__istartswith=self.q).order_by("first_name", "last_name")
