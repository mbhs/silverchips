from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class SmallThumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 60}


class MediumThumbnail(ImageSpec):
    processors = [ResizeToFill(300, 300)]
    format = 'JPEG'
    options = {'quality': 60}


class LargeThumbnail(ImageSpec):
    processors = [ResizeToFill(600, 600)]
    format = 'JPEG'
    options = {'quality': 70}


class HugeThumbnail(ImageSpec):
    processors = [ResizeToFill(800, 800)]
    format = 'JPEG'
    options = {'quality': 80}


register.generator("home:small_thumbnail", SmallThumbnail)
register.generator("home:medium_thumbnail", MediumThumbnail)
register.generator("home:large_thumbnail", LargeThumbnail)
register.generator("home:huge_thumbnail", HugeThumbnail)
