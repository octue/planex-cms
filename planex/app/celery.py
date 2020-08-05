import logging
import os
from django.conf import settings


print(repr(settings.KOMBU_FERNET_KEY))
print(repr(os.environ["KOMBU_FERNET_KEY"]))

from celery import Celery  # noqa:E402
from django.apps import AppConfig  # noqa:E402


app = Celery("app")


logger = logging.getLogger(__name__)


class CeleryConfig(AppConfig):
    name = "app"
    verbose_name = "Celery Config"

    def ready(self):
        # Using a string here means the worker will not have to pickle the object when using Windows
        app.config_from_object("django.conf:settings", namespace="CELERY")

        # TODO Override any task serialisation to ensure that secure communication is used, as per:
        # https://blog.heroku.com/securing-celery
        # Understand the role these play (they currently produce a TypeError):
        # from kombu_fernet.serializers.json import MIMETYPE
        # app.conf.update(
        #             CELERY_TASK_SERIALIZER='fernet_json',
        #             CELERY_RESULT_SERIALIZER='fernet_json',
        #             CELERY_ACCEPT_CONTENT=[MIMETYPE],
        #         )

        # Load task modules from all registered Django app configs
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
