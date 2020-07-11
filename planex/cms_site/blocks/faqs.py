from wagtail.core.blocks import CharBlock, ListBlock, StructBlock, TextBlock, URLBlock

from .base import SectionBlock
from .material_icons import IconChoiceBlock


class FaqBlock(StructBlock):
    question = CharBlock(
        required=True,
        max_length=80,
        label="Question",
        help_text="Add a simply worded question, like 'How much will it cost?'",
    )
    answer = TextBlock(
        required=True, label="Answer", help_text="Provide a short answer in no more than a few lines of text"
    )
    icon = IconChoiceBlock(
        required=False, label="Icon", help_text="Pick an icon (see https://material.io/tools/icons/) for a bullet point"
    )
    more_info_url = URLBlock(
        required=False,
        label="URL",
        help_text="Add a link to be followed for more information on that question, feature or product",
    )

    class Meta:
        icon = "help"
        label = "FAQ"


class FaqSectionBlock(SectionBlock):
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
    faqs = ListBlock(FaqBlock(), label="FAQs")

    class Meta:
        icon = "help"
        label = "FAQs Section"
