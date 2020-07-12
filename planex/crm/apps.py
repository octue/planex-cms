from django.apps import AppConfig


class CRMAppConfig(AppConfig):
    name = "crm"
    label = "crm"
    verbose_name = "CRM (HubSpot)"

    def ready(self):
        # import crm_hubspot.signals
        pass
