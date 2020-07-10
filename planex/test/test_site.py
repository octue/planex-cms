from collections import OrderedDict
from wagtail.core.models import Page


from .base import BaseGrappleTestCase


class PagesTest(BaseGrappleTestCase):
    def test_pages(self):
        query = """
        {
            pages {
                title
            }
        }
        """
        executed = self.client.execute(query)

        self.assertEquals(type(executed["data"]), OrderedDict)
        self.assertEquals(type(executed["data"]["pages"]), list)
        self.assertEquals(type(executed["data"]["pages"][0]), OrderedDict)

        pages = Page.objects.all()

        self.assertEquals(len(executed["data"]["pages"]), pages.count())
