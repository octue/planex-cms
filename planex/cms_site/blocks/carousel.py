from wagtail.core.blocks import CharBlock, ListBlock, StructBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

from .base import SectionBlock


class CarouselImageBlock(StructBlock):
    image = ImageChooserBlock()
    link_url = URLBlock(required=False, label="Link URL")

    class Meta:
        icon = "image"
        label = "Carousel Image"


class CarouselSectionBlock(SectionBlock):
    heading = CharBlock(
        required=False,
        max_length=100,
        label="Section Heading",
        help_text="Add a heading at the beginning of this page section",
    )
    description = TextBlock(
        required=False,
        max_length=400,
        label="Section Description",
        help_text="Provide a slightly more detailed description of what this section is for",
    )
    # TODO enable carousel of more than just images - e.g. any section
    images = ListBlock(CarouselImageBlock(), label="Images")

    class Meta:
        icon = "image"
        label = "Carousel Section"
