from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from .base import SectionBlock


class HeroSectionBlock(SectionBlock):
    heading = CharBlock(required=False, max_length=100, label="Hero Heading", help_text="Add the big hero text. Keep it snappy.", default="We are heroes")
    description = TextBlock(
        required=False,
        max_length=400,
        label="Hero Description",
        help_text="Add a couple of lines under the hero text",
        default="Here is a list of our Head Peeps. They look glorious here but are probably just normal, mortal humans.",
    )
    image = ImageChooserBlock(required=False, label="Hero image")
    content = StreamBlock(
        [
            (
                "button",
                StructBlock(
                    [("text", CharBlock(required=False, max_length=80, label="Label")), ("url", URLBlock(required=False, label="URL")),],
                    required=False,
                    label="Call to action",
                    help_text='A "call-to-action" button, like "Sign Up Now!"',
                ),
            ),
            ("video", EmbedBlock(required=False, label="Video")),
            (
                "quote",
                StructBlock(
                    [("text", TextBlock()), ("author", CharBlock(required=False)),],
                    required=False,
                    label="Quote",
                    help_text="An inspiring quotation, optionally attributed to someone",
                ),
            ),
        ],
        required=False,
        block_counts={"button": {"max_num": 1}, "video": {"max_num": 1}, "quote": {"max_num": 1}},
    )

    class Meta:
        icon = "placeholder"
        label = "Hero Section"
