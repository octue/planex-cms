from wagtail.core.blocks import BlockQuoteBlock, CharBlock, RawHTMLBlock, RichTextBlock, StreamBlock, TextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock

from .base import SectionBlock


class GeneralSectionBlock(SectionBlock):
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

    content = StreamBlock(
        [
            (
                "image",
                ImageChooserBlock(
                    required=False,
                    label="Image",
                    help_text="An image that will appear appear centred as a section of page content, with its caption and accreditation.",
                ),
            ),
            (
                "quote",
                BlockQuoteBlock(
                    required=False,
                    label="Quote",
                    help_text="A quote that will appear as a block section of page content, with an attribution line beneath.",
                ),
            ),
            ("rich_text", RichTextBlock(required=False, label="Body (rich text)", help_text="Rich text based input.")),
            ("raw_html", RawHTMLBlock(required=False, label="Raw HTML", help_text="Raw HTML")),
            ("embed", EmbedBlock(required=False, label="Embed", help_text="Select embedded media")),
            (
                "markdown",
                MarkdownBlock(
                    required=False,
                    label="Body (markdown)",
                    help_text="Use markdown to provide generalised body content (including bold, italic, links, syntax highlights, etc)",
                ),
            ),
        ],
        blank=True,
        help_text="Section contents",
    )

    class Meta:
        icon = "placeholder"
        label = "General Section"
