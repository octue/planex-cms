from django.urls import path

from cms_core import views


urlpatterns = [
    path("newsletter-subscribe", views.newsletter_subscribe),
]
