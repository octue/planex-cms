from wagtail.core.blocks import CharBlock, ListBlock, StructBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

from .base import SectionBlock


class CardBlock(StructBlock):
    title = CharBlock(
        required=True,
        max_length=80,
        label="Name",
        help_text="Name of a product. Keep it short, like 'Mega Kit Pro' or 'Cloud Manager'",
    )
    body = TextBlock(
        required=True, max_length=400, label="Description", help_text="Write a few lines about this product"
    )
    image = ImageChooserBlock(required=False, label="Image", help_text="Pick an image to represent this product")
    more_info_url = URLBlock(required=False, label="URL", help_text="A link to be followed for more information")

    class Meta:
        icon = "tick-inverse"
        label = "Card contents"


class CardSectionBlock(SectionBlock):
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
    cards = ListBlock(CardBlock(), label="Features")

    class Meta:
        icon = "list-ul"
        label = "Cards Section"
