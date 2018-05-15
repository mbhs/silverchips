"""Some template tags and filters shared between the public and staff sides of the website."""

from django import template
from core import permissions

register = template.Library()

# Setup permission checking filters for each permission for content
for action in permissions.CONTENT_ACTIONS:
    @register.filter("can_{}_content".format(action))
    def can(user, content, action=action):
        """A filter that checks whether a user can {} a particular Content.""".format(action)
        return permissions.can(user, "content.{}".format(action), content)


@register.filter("can")
def can(user, permission):
    """A filter that checks whether a user has a given permission in Django's permission scheme."""
    return user.has_perm(permission)
