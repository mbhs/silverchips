from django.contrib.auth.decorators import user_passes_test
from core.models import User, Content


def can_read(user: User, content: Content):
    """Check whether a particular user has read-access to particular content."""

    # Published content can be read publicly
    if content.visibility == Content.PUBLISHED:
        return True

    if user is not None:
        # Editors can read all content
        if user.has_role("editor"):
            return True

        if user.has_role("writer"):
            # Writers can read all pending content
            if content.visibility == Content.PENDING:
                return True

            # Writers can read their own drafting content
            if content.visibility == Content.DRAFT and user in content.authors:
                return True

    return False


def read_access_required(content):
    """A decorator for Django views that tests whether the user has read-access to particular content."""
    return user_passes_test(lambda user: can_read(user, content))
