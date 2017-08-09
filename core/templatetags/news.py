from django import template

from core.models import Story

register = template.Library()


@register.simple_tag
def render_content(content):
    tmp = template.loader.get_template(content.template)
    context = {"content": content}

    return tmp.render(context)


@register.filter
def stories(section):
    return