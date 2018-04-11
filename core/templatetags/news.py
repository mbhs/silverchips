from django import template
import re

from core.models import Content

register = template.Library()


# A template tag that renders the template of some content, for example, story text or an image with a caption
@register.simple_tag
def render_content(content):
    return template.loader.get_template("content/embed.html").render({"content": content})


# A filter that expands embedding tags in story HTML
# For example, <sco:embed type="image" id=3734/> will be replaced with the rendered HTML template of Image #3734
@register.filter
def expand_embeds(text):
    def replace(match):
        return render_content(Content.objects.get(pk=int(match.group(1))))

    text = re.sub("<sco:embed id=(\d+)/>", replace, text)
    return text
