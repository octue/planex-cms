from django.db.models import CASCADE, CharField, ForeignKey
from grapple.models import GraphQLImage, GraphQLString
from wagtail.images.models import AbstractImage, AbstractRendition, Image


class AccreditedImage(AbstractImage):
    """
    AccreditedImage - Customised image model with optional caption and accreditation
    """

    # Database fields
    caption = CharField(max_length=255, blank=True)
    accreditation = CharField(max_length=255, blank=True, null=True)
    admin_form_fields = Image.admin_form_fields + ("caption", "accreditation",)
    graphql_fields = [
        GraphQLString("caption"),
        GraphQLString("accreditation"),
    ]

    class Meta:
        verbose_name = "Accredited image"
        verbose_name_plural = "Accredited images"

    def __str__(self):
        credit = (
            " ({})".format(self.accreditation)
            if (self.accreditation is not None) and (len(self.accreditation) > 0)
            else ""
        )
        return "{}{}".format(self.title, credit)


class AccreditedRendition(AbstractRendition):
    """
    AccreditedRendition - stores renditions for the AccreditedImage model
    """

    # Database fields
    image = ForeignKey(AccreditedImage, on_delete=CASCADE, related_name="renditions")

    graphql_fields = (
        GraphQLString("id"),
        GraphQLString("url"),
        GraphQLString("width"),
        GraphQLString("height"),
        GraphQLImage("image"),
        GraphQLString("file"),
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
        verbose_name = "Accredited Image Rendition"
        verbose_name_plural = "Accredited Image Renditions"
