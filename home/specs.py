from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit


class SmallThumbnail(ImageSpec):
    processors = [ResizeToFit(100, 100)]


class MediumThumbnail(ImageSpec):
    processors = [ResizeToFit(250, 250)]


class LargeThumbnail(ImageSpec):
    processors = [ResizeToFit(500, 500)]


class HugeThumbnail(ImageSpec):
    processors = [ResizeToFit(800, 800)]


register.generator("home:small_thumbnail", SmallThumbnail)
register.generator("home:medium_thumbnail", MediumThumbnail)
register.generator("home:large_thumbnail", LargeThumbnail)
register.generator("home:huge_thumbnail", HugeThumbnail)
