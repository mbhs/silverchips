from bs4 import BeautifulSoup
from django import template
from django.utils.html import mark_safe, format_html
from imagekit.cachefiles import ImageCacheFile

from core import permissions, models
from home.imagegenerators import (
    SmallThumbnail,
    MediumThumbnail,
    LargeThumbnail,
    HugeThumbnail,
)
from silverchips.settings import STATIC_URL

register = template.Library()


@register.filter
def thumb(content, thumb_type=None):
    """A filter to return an image file used to preview a Content as a thumbnail.

    The particular image selected depends on the type of Content.
    """
    image = None  # The ImageField that we're using as a source for the thumbnail

    if (
        isinstance(content, models.Story) or isinstance(content, models.Video)
    ) and content.cover:
        image = content.cover.source
    elif isinstance(content, models.Image):
        image = content.source
    elif isinstance(content, models.Gallery) and content.entries.count() > 0:
        # Gallery cache currently messed up, so no thumbnail for now
        # image = thumb(content.entries_in_order()[0])
        return content.entries_in_order()[0].source.url

    if image is None:
        return None

    if thumb_type is None:
        return True

    # Check which thumbnail generator we're using
    klass = {
        "small": SmallThumbnail,
        "medium": MediumThumbnail,
        "large": LargeThumbnail,
        "huge": HugeThumbnail,
    }[thumb_type]

    # Make the thumbnail generator and cache the result
    try:
        generator = klass(source=image)
        cached_file = ImageCacheFile(generator)
        cached_file.generate()  # This seems to be necessary to save the file
        return cached_file.url
    except FileNotFoundError:
        return None
    except (IOError, SyntaxError):  # Error actually parsing the file
        return image.url


@register.filter
def qualified_title(content):
    """A filter to qualify non-story Content with a descriptive prefix (e.g. Photo:)."""
    if isinstance(content, models.Story):
        return mark_safe(content.title)
    else:
        return mark_safe("{}: {}".format(content.descriptor, content.title))


@register.simple_tag(takes_context=True)
def render_content(context, user, content, embedding=True):
    """A template tag that renders the template of some Content, for example, story text or an image with a caption.

    Only works when user has read permissions on the content object.
    """
    computed_content = (
        content if content and permissions.can(user, "content.read", content) else None
    )
    return template.loader.get_template("home/content/display.html").render(
        {
            "content": computed_content,
            "user": user,
            "embedding": embedding,
        },
        context.request,
    )


@register.simple_tag(takes_context=True)
def expand_embeds(context, text, user):
    """A filter that expands embedding tags in story HTML.

    For example, the contents of <div class="embed-content" data-content-id="3734"/>
    will be expanded with the rendered HTML template of content #3734. This code uses
    the BeautifulSoup library to parse the story HTML and find matching divs.
    """
    soup = BeautifulSoup(text, "html.parser")

    # Find all <div class="content-embed">s
    for div in soup.findAll("div"):
        if div.has_attr("class") and "content-embed" in div["class"]:
            # Try and load the content corresponding to data-contend-id on each div
            pk = int(div["data-content-id"])
            try:
                content = models.Content.objects.get(pk=pk)
            except models.Content.DoesNotExist:
                content = None
            # Render that content for the particular user
            html = render_content(context, user, content)
            # Insert the rendered html into the div
            div.insert(0, BeautifulSoup(html, "html.parser"))

    return mark_safe(str(soup))


@register.filter
def first_or_self(val):
    """A filter that returns the first element of the value if it's a list, otherwise it returns the value itself.

    For example, [1, 2, 3] becomes 1, while 1 remains 1.
    """
    if isinstance(val, list) or isinstance(val, tuple):
        return val[0]
    return val


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
        reserved_content = context.get("_reserved_content", set())

        # Load new, non-reserved content from the database
        new_content = content.exclude(pk__in=reserved_content)[: self.count]

        # Reserve the content we just loaded
        reserved_content.update(new_content.values_list("pk", flat=True))

        if len(new_content) == self.count == 1:
            new_content = new_content[0]

        context["new_content"] = new_content

        # Force setting as global variable by placing variable in all levels of context stack
        for context_dict in context.dicts:
            context_dict["_reserved_content"] = reserved_content

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


class ObfuscatedEmailNode(template.Node):
    """Template tag node to represent an obfuscated email to avoid automated scrapers.

    This tag works by forcing a hidden variable called `_has_obfuscated_emails` into the entire template context stack."""

    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        # Force setting as global variable by placing variable in all levels of context stack
        for context_dict in context.dicts:
            context_dict["_has_obfuscated_emails"] = True

        return format_html(
            '<a data-email="{}" class="obfuscated-email" href="loading">loading...</a>',
            "".join(chr(ord(x) ^ 1) for x in self.email.resolve(context)),
        )


class EmailDeobfuscatorNode(template.Node):
    """Template tag node to render the script that deobfuscates obfuscated emails.

    A script tag will only be rendered if the `_has_obfuscated_emails` variable has been set."""

    def __init__(self):
        pass

    def render(self, context):
        if context.get("_has_obfuscated_emails") == True:
            return format_html(
                '<script async defer src="{}"></script>',
                STATIC_URL + "home/scripts/emails.js",
            )
        return ""


@register.tag
def obfuscated_email(parser, token):
    tag_name, email = token.split_contents()
    return ObfuscatedEmailNode(email)


@register.tag
def email_deobfuscator(parser, token):
    (tag_name,) = token.split_contents()
    return EmailDeobfuscatorNode()
