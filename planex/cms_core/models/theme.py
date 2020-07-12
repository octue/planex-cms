from django.core.serializers.json import DjangoJSONEncoder
from grapple.models import GraphQLString
from jsoneditor.fields.postgres_jsonfield import JSONField
from jsoneditor.forms import JSONEditor
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class ThemeSettings(BaseSetting):
    """ Allows you to override a material ui theme with a json object
    """

    theme = JSONField(
        null=False,
        default=dict,
        encoder=DjangoJSONEncoder,
        help_text="Paste a JSON object containing material ui theme options",
    )

    panels = [
        FieldPanel("theme", widget=JSONEditor),
    ]

    graphql_fields = [
        GraphQLString("theme"),
    ]
