from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^contact/$", views.contact.ContactFormView.as_view(), name="contact"),
    url(r"^subscribe/$", views.subscribe.SubscribeFormView.as_view(), name="subscribe"),
]
