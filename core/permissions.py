from core.models import Content, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin

# TODO: implement draft

CONTENT_ACTIONS = ['read', 'edit', 'delete', 'pend', 'publish', 'hide']
VISIBILITY_ACTIONS = {Content.DRAFT: 'content.draft', Content.PENDING: 'content.pend',
                      Content.PUBLISHED: 'content.publish', Content.HIDDEN: 'content.hide'}

USER_ACTIONS = ['manage', 'edit_profile']


def can(user, action, obj):
    """Master object-level permission logic for the entire backend.

    This function allows us to check whether a given user has permission
    to perform a given "action" on a particular "object". This can depend
    both on the permissions of the user and on properties of the object.
    Actions will take the form "<type>.<type_action>", such as "content.edit".
    """

    _type, action = action.split('.')

    if _type == 'content':
        assert isinstance(obj, Content)

        # This is the only action that can take place without any authentication
        if action == 'read':
            return obj and (obj.visibility == Content.PUBLISHED or user is not None and user.has_perm('core.read_content'))

        if user is None or not user.is_active:
            return False

        if action == 'edit':
            return obj.visibility == Content.DRAFT and user in obj.authors.all() and user.has_perm(
                'core.draft_content') \
                   or (
                               Content.DRAFT <= obj.visibility or obj.visibility == Content.HIDDEN and user.has_perm(
                                'hide_content')) and user.has_perm('core.edit_content')
        if action == 'delete':
            return (obj.visibility == Content.DRAFT and user in obj.authors.all() and user.has_perm(
                'core.draft_content')) or user.has_perm('core.delete_content')
        if action == 'pend':
            return obj.visibility == Content.DRAFT and (
                    (user in obj.authors.all() and user.has_perm('core.draft_content')) or user.has_perm(
                        'core.edit_content')) \
                   or obj.visibility == Content.PUBLISHED and user.has_perm('core.publish_content') \
                   or obj.visibility == Content.HIDDEN and user.has_perm('core.hide_content')
        if action == 'publish':
            return (obj.visibility == Content.PENDING or (
                    obj.visibility == Content.HIDDEN and user.has_perm('code.hide_content'))) and user.has_perm(
                'core.publish_content')
        if action == 'hide':
            return obj.visibility != Content.HIDDEN and user.has_perm('core.hide_content')
    if _type == 'users':
        assert isinstance(obj, User)

        if user is None or not user.is_active:
            return False

        if action == 'manage':
            return user.has_perm('auth.manage_users')
        if action == 'edit_profile':
            return user.has_perm('auth.manage_users') or user == obj and user.has_perm('core.edit_profile')

    return False


def check_permission(user, action, pk):
    """Helper function to check whether a user has permission to perform an action on an object, identified numerically.

    This simply is convenient for use in views to check permissions.
    """
    t, _ = action.split('.')
    if t == 'content':
        obj = Content.objects.get(pk=pk)
    if t == 'users':
        obj = User.objects.get(pk=pk)
    return can(user, action, obj)


def user_can(action):
    """A decorator for views that tests whether a user can perform an object-level action."""
    def wrapper(view_func):
        def view(request, **kwargs):
            pk = kwargs['pk']

            # If the user cannot perform the action, complain
            if not check_permission(request.user, action, pk):
                raise PermissionDenied

            return view_func(request, **kwargs)
        return view
    return wrapper


class UserCanMixin(AccessMixin):
    """A mixin for class-based views that tests whether a user can perform an object-level action."""
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']

        # If the user cannot perform the action, complain
        if not check_permission(request.user, self.action, pk):
            return self.handle_no_permission()

        return super().dispatch(request, **kwargs)
