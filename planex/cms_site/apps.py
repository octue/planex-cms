from django.apps import AppConfig


class CMSSiteAppConfig(AppConfig):
    name = "cms_site"
    label = "cms_site"
    verbose_name = "Site"

    def ready(self):
        # import cms_site.signals
        pass
