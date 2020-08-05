from collections import OrderedDict

from .base import BaseGrappleTestCase


# from planex.cms_core.models import AccreditedImage


class ImagesTest(BaseGrappleTestCase):
    def test_images(self):
        query = """
        {
          imageType
          images {
            aspectRatio
            accreditation
            caption
            src
            id
            width
            height
            sizes
            rendition {
              width
              height
              sizes
              src
              url
            }
          }
        }
        """
        executed = self.client.execute(query)

        self.assertEquals(type(executed["data"]), OrderedDict)
        self.assertEquals(type(executed["data"]["images"]), list)
        # self.assertEquals(type(executed["data"]["images"][0]), OrderedDict)

        # images = AccreditedImage.objects.all()
        #
        # self.assertEquals(len(executed["data"]["images"]), images.count())
