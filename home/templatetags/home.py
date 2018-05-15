from django import template
from django.utils.html import mark_safe
import re

from core.models import Content
from core import permissions

register = template.Library()


@register.simple_tag
def render_content(user, content):
    """A template tag that renders the template of some content, for example, story text or an image with a caption."""
    return template.loader.get_template("home/content/embed.html").render({
        "content": content if content and permissions.can(user, 'content.read', content) else None,
        "user": user
    })


@register.filter
def expand_embeds(text, user):
    """A filter that expands embedding tags in story HTML.

    For example, <sco:embed id=3734/> will be replaced with the rendered HTML template of content #3734.
    """
    def replace(match):
        try:
            content = Content.objects.get(pk=int(match.group(1)))
        except Content.DoesNotExist:
            content = None
        return render_content(user, content)

    text = re.sub("<sco:embed id=(\d+)/>", replace, text)
    return mark_safe(text)
