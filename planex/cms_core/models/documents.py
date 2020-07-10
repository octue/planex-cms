from django.db.models import CharField, TextField
from wagtail.documents.models import Document, AbstractDocument


class AccreditedDocument(AbstractDocument):
    """
    AccreditedDocument - Customised document model with optional accreditation
    """

    # Database fields
    accreditation = CharField(max_length=255, blank=True, null=True)
    description = TextField(max_length=400, blank=True)

    # Wagtail configuration
    admin_form_fields = Document.admin_form_fields + ("accreditation", "description",)

    class Meta:
        verbose_name = "Accredited document"
        verbose_name_plural = "Accredited documents"

    def __str__(self):
        credit = " ({})".format(self.accreditation) if (self.accreditation is not None) and (len(self.accreditation) > 0) else ""
        return "{}{}".format(self.title, credit)
