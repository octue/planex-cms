from django.utils.encoding import force_str
from django.utils.translation import ugettext as _
from fontawesome_5.forms import IconFormField
from wagtail.core.blocks import CharBlock


# from grapple.helpers import register_streamfield_block
# from grapple.models import GraphQLCollection, GraphQLEmbed, GraphQLString


class IconBlock(CharBlock):
    """ An IconBlock corresponding to IconField from the django_fontawesome_5 library.
    """

    class Meta:
        icon = "image"
        label = "Icon (font awesome 5)"

    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        self.field = IconFormField(
            required=required,
            help_text=help_text or _("Choose a fontawesome icon"),
            max_length=60,
            validators=validators,
        )
        super().__init__(**kwargs)

    def get_searchable_content(self, value):
        return [force_str(value)]
