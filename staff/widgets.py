from django.forms.widgets import Widget


class RichTextWidget(Widget):
    """A form input widget that uses quill.js's rich text input facilities."""

    template_name = 'shared/richtext.html'

    def __init__(self, short=False, **kwargs):
        super(RichTextWidget, self).__init__(**kwargs)
        self.attrs['short'] = short
