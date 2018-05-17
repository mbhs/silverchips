"""Custom user authentication.

This module is purely to change the backend authenticator for Users.
Instead of Django authenticated Users, it uses core Users.
"""


# Local models
from django.contrib.auth import backends
from . import models

backends.UserModel = models.User


class ProxiedAllowAllUsersModelBackend(backends.AllowAllUsersModelBackend):
    """Create a model backend for the user proxy.

    This is kind of a hack but is also reasonably clean. It basically
    allows us to maintain features from the user proxy in the core
    models, such as the `get_role` and `__str__` methods, while not
    altering the settings `AUTH_USER_MODEL` property.
    """

    pass
