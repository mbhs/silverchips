from django import template
import re

from core.models import Content

register = template.Library()


@register.simple_tag
def render_content(content):
    return template.loader.get_template("content/embed.html").render({"content": content})


@register.filter
def expand_embeds(text):
    return re.sub("<sco:embed id=(\d+)/>", lambda pk: render_content(Content.objects.get(pk=pk)), text)
