from wagtail.core.blocks import CharBlock, ListBlock, StructBlock, TextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

from .base import SectionBlock
from .material_icons import IconChoiceBlock


class FeatureBlock(StructBlock):
    feature_name = CharBlock(
        required=True,
        max_length=80,
        label="Feature Name",
        help_text="Feature name. Keep it short, like 'Free Chat' or 'Secure'",
    )
    feature_description = TextBlock(
        required=True, max_length=400, label="Feature Description", help_text="Write a few lines about this feature"
    )
    # TODO turn this icon into a bullet image
    icon = IconChoiceBlock(
        required=True, label="Icon", help_text="Pick an icon (see https://material.io/tools/icons/) for a bullet point"
    )
    more_info_url = URLBlock(required=False, label="URL", help_text="A link to be followed for more information")

    class Meta:
        icon = "tick-inverse"
        label = "Feature Description"


class FeatureSectionBlock(SectionBlock):
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
    image = ImageChooserBlock(
        required=False,
        label="Image",
        help_text="Pick an image (e.g. of the product) for the side panel of a feature list",
    )
    features = ListBlock(FeatureBlock(), label="Features")

    class Meta:
        icon = "list-ul"
        label = "Features Section"
