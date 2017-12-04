from django import template
import re

from core.models import Image

register = template.Library()


@register.simple_tag
def render_content(content):
    print(content)
    return template.loader.get_template("content/embed.html").render({"content": content})


@register.filter
def expand_embeds(text):
    print(text)
    return re.sub("<sco:image id=(\d+)/>",
                  lambda match: render_content(Image.objects.get(pk=int(match.group(1)))), text)
