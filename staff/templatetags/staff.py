from django import template

register = template.Library()


@register.filter
def names(content):
    """A filter that returns the full names, joined by commas, of all the authors of a particular Content."""
    return ", ".join(map(lambda user: user.get_full_name(), content.authors.all()))


@register.simple_tag(name='range')
def do_range(start, end, step):
    return list(range(start, end, step))