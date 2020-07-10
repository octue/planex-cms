from django.apps import AppConfig


class CMSCoreAppConfig(AppConfig):
    name = "cms_core"
    label = "cms_core"
    verbose_name = "CMS Core"

    def ready(self):
        # import cms_core.signals
        pass
