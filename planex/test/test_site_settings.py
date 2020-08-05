# from collections import OrderedDict
# from wagtail.core.models import Page

from .base import BaseGrappleTestCase


class SiteSettingsTest(BaseGrappleTestCase):
    def test_empty_theme_json(self):
        pass

        # query = """
        # {
        #     theme
        # }
        # """
        # executed = self.client.execute(query)
        # print(executed)
        # self.assertEquals(type(executed["data"]), OrderedDict)
        # self.assertEquals(type(executed["data"]["theme"]), str)

        # pages = Page.objects.all()
        #
        # self.assertEquals(len(executed["data"]["pages"]), pages.count())
