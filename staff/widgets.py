from django.forms.widgets import Widget
from staff import forms


class RichTextWidget(Widget):
    """A form input widget that uses quill.js's rich text input facilities."""

    template_name = "staff/includes/richtext.html"

    def __init__(self, short=False, embed=False, **kwargs):
        super(RichTextWidget, self).__init__(**kwargs)
        self.attrs["short"] = short
        self.attrs["embed"] = embed

    # Make sure that the widget includes appropriate files for Quill
    class Media:
        css = {
            "all": (
                "https://cdn.quilljs.com/1.3.4/quill.core.css",
                "https://cdn.quilljs.com/1.3.4/quill.snow.css",
            )
        }
        js = ("https://cdn.quilljs.com/1.3.4/quill.js", "staff/scripts/quill.js")
