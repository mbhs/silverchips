from django import template
import re

from core.models import Content

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