from django import template

register = template.Library()


@register.simple_tag
def render_content(content):
    tmp = template.loader.get_template(content.template)
    context = {"content": content}

    return tmp.render(context)
