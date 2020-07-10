from wagtail.core.blocks import StructBlock, ListBlock, CharBlock, TextBlock, URLBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from .base import SectionBlock


class TeamMemberBlock(StructBlock):
    name = CharBlock(required=True, max_length=80, label="Name")
    image = ImageChooserBlock(required=True, label="Photo")
    role = CharBlock(required=True, max_length=80, label="Role / Job Title")
    biography = TextBlock(required=False, label="Bio")
    linkedin = URLBlock(required=False, label="LinkedIn Page")
    twitter = URLBlock(required=False, label="Twitter Page")
    github = URLBlock(required=False, label="GitHub Page")
    medium = URLBlock(required=False, label="Medium Page")

    class Meta:
        icon = "user"
        label = "Team Member"


class TeamSectionBlock(SectionBlock):
    heading = CharBlock(
        required=False, max_length=100, label="Section Heading", help_text="Add a heading at the beginning of this page section", default="Our Amazing Team"
    )
    description = TextBlock(
        required=False,
        max_length=400,
        label="Section Description",
        help_text="Provide a slightly more detailed description of what this section is for",
        default="Here is a list of our Head Peeps. They look glorious here but are probably just normal, mortal humans.",
    )
    members = ListBlock(TeamMemberBlock(), label="Team Members")

    class Meta:
        icon = "group"
        label = "Team Section"
