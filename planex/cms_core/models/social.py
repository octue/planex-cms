from django.db import models
from grapple.models import GraphQLString
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSetting):
    """ Social media setting
    """

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    github = models.URLField(blank=True, null=True, help_text="GitHub URL")
    instagram = models.URLField(blank=True, null=True, help_text="Instagram URL")
    linked_in = models.URLField(blank=True, null=True, help_text="LinkedIn URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("github"),
                FieldPanel("instagram"),
                FieldPanel("linked_in"),
                FieldPanel("twitter"),
                FieldPanel("youtube"),
            ],
            heading="Social Media Settings",
        )
    ]

    graphql_fields = [
        GraphQLString("facebook"),
        GraphQLString("github"),
        GraphQLString("instagram"),
        GraphQLString("linked_in"),
        GraphQLString("twitter"),
        GraphQLString("youtube"),
    ]
