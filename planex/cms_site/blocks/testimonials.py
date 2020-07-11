from wagtail.core.blocks import CharBlock, ChoiceBlock, ListBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from .base import SectionBlock


class TestimonialBlock(StructBlock):
    name = CharBlock(
        required=True, max_length=100, label="Name", help_text="Name of the person making the recommendation"
    )
    role = CharBlock(
        required=False,
        max_length=100,
        label="Role",
        help_text="Job title of the person making the recommentation, if any",
    )
    organisation = CharBlock(
        required=False,
        max_length=100,
        label="Organisation",
        help_text="Name of the organisation the person is part of, if any",
    )
    quote = TextBlock(required=True, max_length=100, label="Quote", help_text="The nice things they have to say")
    image = ImageChooserBlock(
        required=False, label="Logo/Picture", help_text="Add either a company logo or a person's mugshot"
    )
    stars = ChoiceBlock(
        required=True,
        choices=[
            (None, "No rating"),
            (0, "0 Stars"),
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ],
        icon="pick",
    )

    class Meta:
        icon = "pick"
        label = "Testimonial"


class TestimonialSectionBlock(SectionBlock):
    heading = CharBlock(
        required=False,
        max_length=100,
        label="Section Heading",
        help_text="Add a heading at the beginning of this page section",
        default="Testimonials",
    )
    description = TextBlock(
        required=False,
        max_length=400,
        label="Section Description",
        help_text="Provide a slightly more detailed description of what this section is for",
        default="Our users love us. Look at these rave reviews...",
    )
    testimonials = ListBlock(TestimonialBlock(), label="Testimonials")

    class Meta:
        icon = "pick"
        label = "Testimonials Section"
