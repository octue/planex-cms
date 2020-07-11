import logging


# import imghdr
# from django_filters import rest_framework as django_filters
# from django.http import HttpResponse, HttpResponsePermanentRedirect, StreamingHttpResponse, JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views import View
# from drf_yasg.inspectors import SwaggerAutoSchema
# from rest_framework import viewsets, filters, permissions
# from wagtail.images import get_image_model
# from wagtail.images.exceptions import InvalidFilterSpecError
# from wagtail.images.models import SourceImageIOError
# from wsgiref.util import FileWrapper
#
# from site.models import Page, AccreditedDocument
# from site.serializers import PageListSerializer, PolymorphicPageSerializer, DocumentSerializer
# from site.polymorphic import PolymorphicSerializerViewSetMixin, PolymorphicSwaggerAutoSchema
# from site.base_viewset import BaseViewSetMixin


logger = logging.getLogger(__name__)


# class ImageServeView(View):
#
#     model = get_image_model()
#     action = 'serve'
#
#     def get(self, request, id):
#         """ NOTE: The wagtail built-in image serve view includes a signature generation, which means that, server-side,
#         you have to define what filters you apply, per image, in order to generate signed URLS, which can then be used to fetch the image.
#
#         This is sensible, because it prevents heavy DDOS attacks which create a new, slightly different, image rendition each time.
#
#         HOWEVER, it violates separation of concerns (you have to specify front end rendering and styling details server-side), and is an
#         especial PITA with a headless CMS, since you have to
#
#         It grows even worse when you don't, a priori, know what image size your front end will want to use. Ideally, your frontend will just
#         fetch an image from the URL it wants, with the filter it wants.
#
#         But how to take care of the too-many-requests problem? Answer: If your site is important enough to worry about this, use
#         throttling (you'll want to define a tighter throttle for this than for most views, being as its heavier processing than most responses).
#         See: https://www.django-rest-framework.org/api-guide/throttling/
#
#         An alternative method would be to define a list of allowed filter methods on this class.
#
#         So here I've rewritten the image serve to avoid generation and comparation of a signature, enabling properly-dynamic image rendition fetching.
#
#         :param request:
#         :param id: Integer PK ID of the image to serve
#         :return:
#         """
#         filter = request.GET.get('filter', None)
#
#         image = get_object_or_404(self.model, id=id)
#
#         # Get/generate the rendition
#         try:
#             if filter is not None:
#                 # Dynamically create a rendition of the image according to filter spec
#                 rendition = image.get_rendition(filter)
#             else:
#                 # If no filter, return the original image
#                 rendition = image
#
#         except SourceImageIOError:
#             return HttpResponse("Source image file not found", content_type='text/plain', status=404)
#
#         except InvalidFilterSpecError:
#             return HttpResponse("Invalid filter spec: " + filter, content_type='text/plain', status=400)
#
#         return getattr(self, self.action)(rendition)
#
#     def serve(self, rendition):
#         """ Open and serve the file
#         """
#         rendition.file.open('rb')
#         image_format = imghdr.what(rendition.file)
#         return StreamingHttpResponse(FileWrapper(rendition.file), content_type='image/' + image_format)
#
#     def redirect(self, rendition):
#         """ Redirect to the file's public location
#         """
#         return HttpResponsePermanentRedirect(rendition.url)
#
#
# class ImageMetaView(View):
#
#     model = get_image_model()
#
#     def get(self, request, id):
#         """ Serves image meta as json
#         :param id: Integer PK ID of the image to serve
#         :return:
#         """
#         image = get_object_or_404(self.model, id=id)
#         return JsonResponse({
#             'id': image.id,
#             'accreditation': image.accreditation,
#             'caption': image.caption,
#         }, status=201)


# class DocumentViewSet(BaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
#     """ API endpoint to list and, retrieve documents
#     """
#     filter_backends = (
#         django_filters.DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     )
#     permission_classes = (permissions.AllowAny,)
#     filter_fields = {'id': ('exact',)}
#     search_fields = ('id', 'title')
#     queryset = AccreditedDocument.objects.all()
#     serializer_class = DocumentSerializer
