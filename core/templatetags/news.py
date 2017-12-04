from django import template
import re

from core.models import Image

register = template.Library()


# A template tag that renders the template of some content, for example, story text or an image with a caption
@register.simple_tag
def render_content(content):
    return template.loader.get_template("content/embed.html").render({"content": content})


# A filter that expands embedding tags in story HTML
# For example, <sco:image id=3734/> will be replaced with the rendered HTML template of Image #3734
@register.filter
def expand_embeds(text):
    def replace(match):
        try:
            if match.group(1) == "image":
                content_type = Image

            return render_content(content_type.objects.get(pk=int(match.group(2))))
        except Exception as e:
            print(e)
            return None

    text = re.sub("<sco:embed type=\"([a-z]+)\" id=(\d+)/>", replace, text)
    return text
