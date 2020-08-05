# from collections import OrderedDict
# from wagtail.core.models import Page

from .base import BaseGrappleTestCase


class SiteTest(BaseGrappleTestCase):
    def test_site_meta(self):
        pass
        # query = """
        #   site {
        #     faviconMetaTags(variants: icon) {
        #       attributes
        #       content
        #       tag
        #     }
        #     globalSeo(locale: en) {
        #       facebookPageUrl
        #       siteName
        #       titleSuffix
        #       twitterAccount
        #       fallbackSeo {
        #         description
        #         title
        #         twitterCard
        #       }
        #     }
        #   }
        # """
        # executed = self.client.execute(query)
        # print(executed)
        # self.assertEquals(type(executed["data"]), OrderedDict)
        # self.assertEquals(type(executed["data"]["pages"]), list)
        # self.assertEquals(type(executed["data"]["pages"][0]), OrderedDict)
        #
        # pages = Page.objects.all()
        #
        # self.assertEquals(len(executed["data"]["pages"]), pages.count())
