from django import template

register = template.Library()


@register.filter
def names(content):
    """A filter that returns the full names, joined by commas, of all the authors of a particular Content."""
    return ", ".join(map(lambda user: user.get_full_name(), content.authors.all()))


@register.simple_tag(name='range')
def do_range(start, end, step):
    """A template tag that can be used to assign a range-list to a variable.

    Usage:
    {% range 1 10 1 as range %}
    {% for i in range %}
        {{ i }}
    {% endfor %}

    renders to 1 2 3 4 5 6 7 8 9
    """
    return list(range(start, end, step))
