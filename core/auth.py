"""Custom user authentication.

This module is purely to change the backend authenticator for Users.
Instead of Django authenticated Users, it uses core Users.
"""


# Local models
from . import models


# Authentication backend
class Backend:
    """A custom authentication for website staff.

    Uses the core User model rather than the provided Django
    authentication one.
    """

    def authenticate(self, username=None, password=None):
        """Authenticate a custom user."""

        # Get the user
        try:
            user = models.User.objects.get(username=username)

        # Except failure
        except models.User.DoesNotExist:
            return None

        # Check the password
        else:
            if user.check_password(password):
                return user

        # Fail but return False instead of None
        return False

    def get_user(self, user_id):
        """Get a user by the User's ID."""

        try:
            return models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            return None
