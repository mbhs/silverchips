from core.models import Content

ACTIONS = ['read', 'edit', 'delete', 'pend', 'publish', 'hide']
VISIBILITY_ACTIONS = {Content.DRAFT: 'draft', Content.PENDING: 'pend', Content.PUBLISHED: 'publish', Content.HIDDEN: 'hide'}

def can(user, action, content):
    """Master permission logic for the entire backend."""
    # This is the only action that can take place without any authentication
    if action == 'read':
        return content.visibility == Content.PUBLISHED or user.has_perm('core.read_content')

    if user is None:
        return False

    if action == 'edit':
        return content.visibility == Content.DRAFT and user in content.authors.all() and user.has_perm(
            'core.draft_content') \
               or (
                           Content.DRAFT <= content.visibility <= Content.PENDING or content.visibility == Content.HIDDEN and user.has_perm(
                       'hide_content')) and user.has_perm('core.edit_content')
    if action == 'delete':
        return (content.visibility == Content.DRAFT and user in content.authors.all() and user.has_perm(
            'core.draft_content')) or user.has_perm('core.delete_content')
    if action == 'pend':
        return content.visibility == Content.DRAFT and (
                (user in content.authors.all() and user.has_perm('core.draft_content')) or user.has_perm(
            'core.edit_content')) \
               or content.visibility == Content.PUBLISHED and user.has_perm('core.publish_content') \
               or content.visibility == Content.HIDDEN and user.has_perm('core.hide_content')
    if action == 'publish':
        return (content.visibility == Content.PENDING or (
                    content.visibility == Content.HIDDEN and user.has_perm('code.hide_content'))) and user.has_perm(
            'core.publish_content')
    if action == 'hide':
        return content.visibility != Content.HIDDEN and user.has_perm('core.hide_content')
