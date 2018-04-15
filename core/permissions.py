from django.contrib.auth.decorators import user_passes_test
from core.models import User, Content


def can_read(user: User, content: Content):
    """Check whether a particular user has read-access to particular content."""

    # Published content can be read publicly
    if content.visibility == Content.PUBLISHED:
        return True

    if user is not None:
        if user.has_perm("silverchips.read_all_content"):
            return True
        if user in content.authors and content.visibility == Content.DRAFT:
            return True

    return False


def can_write(user: User, content: Content):
    """Check whether a particular user has write-access to particular content."""

    if user is not None:
        if user.has_perm("silverchips.edit_all_content"):
            return True
        if user in content.authors and user.has_perm("silverchips.edit_own_content"):
            return True

    return False
