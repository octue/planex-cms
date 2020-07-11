from pydoc import locate
from django.conf import settings
from django.test import TestCase
from graphene.test import Client


SCHEMA = locate(settings.GRAPHENE["SCHEMA"])


class BaseGrappleTestCase(TestCase):
    def setUp(self):
        self.client = Client(SCHEMA)
