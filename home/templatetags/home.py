from bs4 import BeautifulSoup
from django import template
from django.utils.html import mark_safe
from imagekit.cachefiles import ImageCacheFile

from core import permissions, models
from home.imagegenerators import SmallThumbnail, MediumThumbnail, LargeThumbnail, HugeThumbnail

register = template.Library()


@register.filter
def thumb(content, thumb_type=None):
    """A filter to return an image file used to preview a Content as a thumbnail.

    The particular image selected depends on the type of Content.
    """
    image = None  # The ImageField that we're using as a source for the thumbnail

    if isinstance(content, models.Story) and content.cover:
        image = content.cover.source
    elif isinstance(content, models.Image):
        image = content.source
    elif isinstance(content, models.Gallery) and content.entries.count() > 0:
        image = thumb(content.entries_in_order()[0])

    if image is None:
        return None

    if thumb_type is None:
        return True

    # Check which thumbnail generator we're using
    klass = {'small': SmallThumbnail, 'medium': MediumThumbnail, 'large': LargeThumbnail, 'huge': HugeThumbnail}[thumb_type]

    # Make the thumbnail generator and cache the result
    generator = klass(source=image)
    cached_file = ImageCacheFile(generator)
    cached_file.generate()  # This seems to be necessary to save the file
    return cached_file.url


@register.filter
def qualified_title(content):
    """A filter to qualify non-story Content with a descriptive prefix (e.g. Photo:)."""
    if isinstance(content, models.Story):
        return mark_safe(content.title)
    else:
        return mark_safe("{}: {}".format(content.descriptor, content.title))


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
    will be expanded with the rendered HTML template of content #3734. This code uses
    the BeautifulSoup library to parse the story HTML and find matching divs.
    """
    soup = BeautifulSoup(text, "html.parser")

    # Find all <div class="content-embed">s
    for div in soup.findAll('div'):
        if "content-embed" in div["class"]:
            # Try and load the content corresponding to data-contend-id on each div
            print(div)
            pk = int(div["data-content-id"])
            try:
                content = models.Content.objects.get(pk=pk)
            except models.Content.DoesNotExist:
                content = None
            # Render that content for the particular user
            html = render_content(user, content)
            # Insert the rendered html into the div
            div.insert(0, BeautifulSoup(html, "html.parser"))

    return mark_safe(soup.prettify())


class ReserveContentNode(template.Node):
    """Template tag node to mark content objects as already seen and therefore "reserved" on a particular page.

    This is to make sure that content is never repeated on a given page. For instance, if a page
    displays both the top overall content in a given section and in each of its subsections, the tag will
    exclude repetition within the subsections of content already reserved and shown in the overall top content of
    the section.

    This tag works by forcing a hidden variable called `_reserved_content` into the entire template context stack.
    The freshly reserved content is available in the variable `new_content`."""
    def __init__(self, content, count):
        self.content = template.Variable(content)
        self.count = int(count)

    def render(self, context):
        content = self.content.resolve(context)

        # The content that's already been reserved, or an empty set if none has been reserved
        reserved_content = context.get('_reserved_content', set())

        # Load new, non-reserved content from the database
        new_content = content.exclude(pk__in=reserved_content)[:self.count]

        # Reserve the content we just loaded
        reserved_content.update(new_content.values_list('pk', flat=True))

        if len(new_content) == self.count == 1:
            new_content = new_content[0]

        context['new_content'] = new_content

        # Force setting as global variable by placing variable in all levels of context stack
        for context_dict in context.dicts:
            context_dict['_reserved_content'] = reserved_content

        return ""


@register.tag
def reserve_content(parser, token):
    """Template tag to mark content objects as already seen and therefore "reserved" on a particular page.

    Usage:
    {% reserve_content content_query_set 10 %}
      -- takes up to 10 items from content_query_set that haven't already been reserved, reserves them, and places
         the freshly reserved content in `new_content`.

    See ReserveContentNode for details."""
    tag_name, content, count = token.split_contents()
    return ReserveContentNode(content, count)
