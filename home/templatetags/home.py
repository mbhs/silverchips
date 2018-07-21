import time

from bs4 import BeautifulSoup
from django import template
from django.utils.html import mark_safe
import re

from core.models import Content
from core import permissions

register = template.Library()


@register.filter
def tags(content):
    return ", ".join(map(str, content.tags.all()))


@register.simple_tag
def render_content(user, content, embedding=True):
    """A template tag that renders the template of some Content, for example, story text or an image with a caption.

    Only works when user has read permissions on the content object.
    """
    return template.loader.get_template("home/content/display.html").render({
        "content": content if content and permissions.can(user, 'content.read', content) else None,
        "user": user,
        "embedding": embedding
    })


@register.filter
def expand_embeds(text, user):
    """A filter that expands embedding tags in story HTML.

    For example, the contents of <div class="embed-content" data-content-id="3734"/>
    will be expanded with the rendered HTML template of content #3734.
    """
    soup = BeautifulSoup(text, "html.parser")
    for div in soup.findAll('div'):
        if "content-embed" in div["class"]:
            pk = int(div["data-content-id"])
            try:
                content = Content.objects.get(pk=pk)
            except Content.DoesNotExist:
                content = None
            html = render_content(user, content)
            div.insert(0, BeautifulSoup(html, "html.parser"))

    return mark_safe(soup.prettify())


# TODO: FIX THIS
@register.simple_tag(takes_context=True)
def see_content(context, content, num_content):
        if 'seen_content' not in context:
            context['seen_content'] = set()
        print(context['seen_content'])
        context['new_content'] = content.exclude(pk__in=list(context['seen_content']))[:num_content]
        context['seen_content'].update(context['new_content'].values_list('pk', flat=True))
        print(context['seen_content'])
        return ""
