import logging
from django.db.models import CASCADE, SET_NULL, BooleanField, CharField, ForeignKey, TextField
from fontawesome_5.fields import IconField
from grapple.models import GraphQLBoolean, GraphQLCollection, GraphQLForeignKey, GraphQLImage, GraphQLInt, GraphQLString
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Orderable, Page
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel


logger = logging.getLogger(__name__)


FOOTER_CHOICES = (
    ("none", "No footer"),
    ("micro", "Micro footer"),
    ("small", "Small Footer"),
    ("big", "Big footer"),
)


class PageSectionsOrderable(Orderable):
    """ This through-model allows us to select and reorder one or more Sections from the *Section snippets
    """

    page = ParentalKey("cms_site.SitePage", on_delete=CASCADE, related_name="sections")
    section = ForeignKey("cms_site.Section", on_delete=CASCADE, related_name="pages")

    panels = [
        SnippetChooserPanel("section"),
    ]

    graphql_fields = [GraphQLInt("page_id"), GraphQLInt("section_id"), GraphQLForeignKey("section", "cms_site.Section")]


class SitePage(Page):
    """ SitePage is used to manage SEO data and general website content including hero banners
    """

    subtitle_text = TextField(
        help_text="A subtitle for the page, which may or may not be shown (depending on page content)", blank=True,
    )

    allow_below_header = BooleanField(
        default=False,
        help_text="Allow the first section to appear beneath the header of the page (useful for hero images)",
    )

    icon = IconField(help_text="Choose a font-awesome icon to associate with the page",)

    background_image = ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=SET_NULL, related_name="+")

    is_panel_page = BooleanField(
        default=False,
        help_text="If true, content will be rendered into a raised central panel instead of straight into the page",
    )

    footer_kind = CharField(
        choices=FOOTER_CHOICES,
        default="none",
        max_length=16,
        help_text="The panel type defined in the front end application",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle_text"),
                FieldPanel("icon"),
                FieldPanel("is_panel_page"),
                FieldPanel("allow_below_header"),
                ImageChooserPanel("background_image"),
            ],
            heading="General Page Properties",
        ),
        InlinePanel("sections", label="Sections"),
        FieldPanel("footer_kind", heading="Page footer kind"),
    ]

    graphql_fields = [
        GraphQLString("subtitle_text"),
        GraphQLBoolean("allow_below_header"),
        GraphQLBoolean("is_panel_page"),
        GraphQLImage("background_image"),
        GraphQLString("icon_class"),
        # GraphQLString("icon"),
        # GraphQLString("footer_kind"),
        # Basic reference to Orderable model
        GraphQLCollection(GraphQLForeignKey, "sections", "cms_site.PageSectionsOrderable"),
    ]

    subpage_types = [
        "SitePage",
    ]

    @property
    def icon_class(self):
        return "{} fa-{}".format(self.icon.style_prefix, self.icon.name) if self.icon else None
