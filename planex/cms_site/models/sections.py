import logging
from django.core.exceptions import ValidationError
from django.db.models import BooleanField, CharField, Model
from django.utils.encoding import force_text
from django.utils.text import slugify
from grapple.models import GraphQLBoolean, GraphQLStreamfield, GraphQLString
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from ..blocks import (
    CardSectionBlock,
    CarouselSectionBlock,
    FaqSectionBlock,
    FeatureSectionBlock,
    HeroSectionBlock,
    TeamSectionBlock,
    TestimonialSectionBlock,
)


# from grapple.models import GraphQLCollection, GraphQLForeignKey, GraphQLSnippet


logger = logging.getLogger(__name__)


@register_snippet
class Section(index.Indexed, Model):
    """ A section to add to a page.

    The base `Section` class is usable in its own right to create page sections.

    The section type can be varied in two ways:
    1. Creating a section from one of the subclassed specialised section types (below)
    2. Specifying section_type as a general string, which matches one of the types specified in the frontend.
        This allows marketers to quickly create and insert sections of arbitrary
        content, built solely on the front end, then add them to the site using their section_type string.
        This speeds up development by allowing marketers to add sections without doing backend engineering to add
        specialised section types

    """

    hash = CharField(
        null=True,
        blank=True,
        max_length=80,
        help_text="Allow navigation to this section within a page. e.g. 'team' allows navigation to /http://your-site.com/about/#team",
    )
    dark = BooleanField(default=False, help_text="Render the section with the dark theme")
    name = CharField(max_length=80, help_text="Name of this section (to refer to in this CMS, not shown on pages)")
    content = StreamField(
        [
            ("hero", HeroSectionBlock(required=False, label="Hero Section", icon="placeholder")),
            ("team", TeamSectionBlock(required=False, label="Team Section", icon="placeholder")),
            ("carousel", CarouselSectionBlock(required=False, label="Carousel Section", icon="placeholder")),
            ("faq", FaqSectionBlock(required=False, label="FAQ Section", icon="placeholder")),
            ("testimonial", TestimonialSectionBlock(required=False, label="Testimonial Section", icon="placeholder")),
            ("feature", FeatureSectionBlock(required=False, label="Feature Section", icon="placeholder")),
            ("card", CardSectionBlock(required=False, label="Card Section", icon="placeholder")),
        ],
        blank=False,
        # TODO Uncomment when https://github.com/wagtail/wagtail/issues/5175 is solved
        #  because a section should only have one SectionBlock.
        #  max_num=1,
        #  min_num=1
    )

    panels = [
        MultiFieldPanel([FieldPanel("name"), FieldPanel("hash"), FieldPanel("dark")], heading="Section Properties"),
        StreamFieldPanel("content", heading="Section Content"),
    ]

    search_fields = [
        index.SearchField("hash", partial_match=True),
        index.SearchField("name", partial_match=True),
    ]

    graphql_fields = [
        GraphQLString("hash"),
        GraphQLBoolean("dark"),
        GraphQLString("name"),
        GraphQLStreamfield("content"),
    ]

    def __str__(self):
        formatted_hash = " #{}".format(self.hash) if self.hash else ""
        return 'Section{} (id={}), "{}"'.format(formatted_hash, self.id, self.name)

    @staticmethod
    def get_clean_hash(value):
        if value:
            return slugify(force_text(value), allow_unicode=False)
        return value

    def clean(self):

        # Validate the hash
        clean_hash = self.get_clean_hash(self.hash)
        if clean_hash != self.hash:
            raise ValidationError('Section hash must be a valid, non-unicode page slug. Try "{}"'.format(clean_hash))

        # Call the superclass cleaning method
        super().clean()
