from django import template
import re

from core.models import Content
from core import permissions

register = template.Library()


@register.simple_tag
def render_content(content):
    """A template tag that renders the template of some content, for example, story text or an image with a caption."""
    return template.loader.get_template("content/embed.html").render({"content": content})


@register.filter
def expand_embeds(text):
    """A filter that expands embedding tags in story HTML.

    For example, <sco:embed id=3734/> will be replaced with the rendered HTML template of content #3734.
    """
    def replace(match):
        return render_content(Content.objects.get(pk=int(match.group(1))))

    text = re.sub("<sco:embed id=(\d+)/>", replace, text)
    return text


@register.filter
def names(content):
    """A filter that returns the full names, joined by commas, of all the authors of a particular Content."""
    return ", ".join(map(lambda user: user.get_full_name(), content.authors.all()))


for action in permissions.ACTIONS:
    @register.filter("can_{}".format(action))
    def can(user, content, action=action):
        """A filter that checks whether a user can {} a particular Content.""".format(action)
        return permissions.can(user, action, content)


@register.simple_tag(name='range')
def do_range(start, end, step):
    return list(range(start, end, step))