import logging
from django import forms
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from crm.hubspot import create_ticket, get_or_create_contact, update_user_name


logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    """ A contact form for website enquiries by users who are not necessarily logged in or even registered
    """

    first_name = forms.CharField(strip=True, required=True)
    last_name = forms.CharField(strip=True, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(strip=False, required=True)

    # TODO add a recaptchafield
    # recaptcha = ReCaptchaField()


class ContactFormView(APIView):
    """ Add a ContactFormView, which responds with some vanilla JSON if the form is POSTed correctly
    """

    # TODO add a checkbox giving consent for us to add them to the newsletter subscription list

    permission_classes = (AllowAny,)

    def post(self, request):
        # Wrap a full try catch block to avoid losing contact messages in the event of an exception.
        # Developers seeing errors raise here should reach out to the contact, apologise for the error and forward to
        # the relevant staff, reassuring that the issue is now fixed!

        # Create a form instance and populate it with data from the request:
        form = ContactForm(request.data)

        # Validate the form data
        if form.is_valid():

            # Get cleaned data and subject line for the support team email
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            subject = "Contact form enquiry from {fn} {ln} ({eml})".format(eml=email, fn=first_name, ln=last_name)

            # Send support team the enquiry email
            to = [recipient[1] for recipient in settings.SUPPORT_TEAM]
            msg = EmailMultiAlternatives(subject, message, email, to)
            msg.send()

            # Create a ticket on hubspot, if an API key is given
            if settings.HUBSPOT_API_KEY is not None:
                try:
                    contact, created = get_or_create_contact(email)
                    update_user_name(email, first_name, last_name)
                    create_ticket(message, "Octue contact form submission", contact)

                except Exception as e:
                    logger.error(e)

            return JsonResponse(
                {"first_name": first_name, "last_name": last_name, "email": email, "message": message},
                status=HTTP_200_OK,
            )

        return JsonResponse(form.errors.as_json(), status=HTTP_400_BAD_REQUEST)
