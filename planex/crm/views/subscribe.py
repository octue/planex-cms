import logging
from django import forms
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from crm.hubspot import get_or_create_contact, subscribe_contact


logger = logging.getLogger(__name__)


class SubscribeForm(forms.Form):
    """ A subscription form for website enquiries by users who are not necessarily logged in or even registered
    """

    email = forms.EmailField(required=True)

    # TODO add a recaptchafield
    # recaptcha = ReCaptchaField()


class SubscribeFormView(APIView):
    """ Add a SubscribeFormView, which responds with some vanilla JSON if the form is POSTed correctly
    """

    permission_classes = (AllowAny,)

    def post(self, request):

        # Create a form instance and populate it with data from the request:
        form = SubscribeForm(request.data)

        # Validate the form data
        if form.is_valid():

            email = form.cleaned_data.get("email")
            try:
                get_or_create_contact(email)
                subscribe_contact(email)

            except Exception as e:
                logger.error(e)

            return JsonResponse({"email": email}, status=HTTP_200_OK)

        return JsonResponse(form.errors.as_json(), status=HTTP_400_BAD_REQUEST)


# TODO Consider subscribing to mailchimp instead of hubspot:
# import requests
# from django.conf import settings
# from django.http import HttpResponse
#
#
# def newsletter_subscribe(request):
#     if request.is_ajax() and request.GET.get("email"):
#         requests.post(
#             "https://us10.api.mailchimp.com/2.0/lists/subscribe",
#             json={
#                 "apikey": settings.MAILCHIMP_KEY,
#                 "id": settings.MAILCHIMP_MAILING_LIST_ID,
#                 "email": {"email": request.GET.get("email")},
#             },
#         )
#     return HttpResponse()
