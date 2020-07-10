# from django.conf.urls import url, include
# from rest_framework import routers

# from planex.site import views


# router = routers.SimpleRouter()
# router.register(r'pages', views.PageViewSet, basename='pages')
# router.register(r'documents', views.DocumentViewSet, basename='documents')


urlpatterns = []
# url(r'^', include(router.urls)),
# url(r'^images/(?P<id>[0-9])/$', views.ImageMetaView.as_view(), name='image_meta'),     # URL returning json metadata follows API endpoint conventions
# url(r'^images/(?P<id>[0-9])/serve/$', views.ImageServeView.as_view(), name='images'),  # URL from which to serve images direct to browser
