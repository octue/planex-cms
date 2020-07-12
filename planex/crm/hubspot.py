import logging
from datetime import datetime
from django.conf import settings
from hubspot3 import Hubspot3
from hubspot3.crm_associations import Definitions as AssociationDefinitions
from hubspot3.error import HubspotNotFound


logger = logging.getLogger(__name__)


if settings.HUBSPOT_API_KEY:
    client = Hubspot3(api_key=settings.HUBSPOT_API_KEY)


def initialise():
    """ Initialise key variables used to create tickets and manage contacts in hubspot
    :return: (support_pipeline, support_stage, subscription_statuses)
    """

    support_pipeline = None
    support_stage = None
    subscription_statuses = None

    try:
        # List of available email subscription types from hubspot
        subscription_types = client.email_subscription.get_subscription_types()
        subscription_statuses = [
            {"id": definition["id"], "subscribed": True, "optState": "OPT_IN"}
            for definition in subscription_types["subscriptionDefinitions"]
        ]

        # The support pipeline to add 'contact' tickets to
        ticket_pipelines = client.crm_pipelines.get_all(object_type="tickets")
        support_pipeline = None
        for pipeline in ticket_pipelines:
            if pipeline["label"] == "Support Pipeline":
                support_pipeline = pipeline["pipelineId"]
                support_stage = pipeline["stages"][0]["stageId"]

        if support_pipeline is None:
            raise Exception('Cannot get "Support Pipeline" from hubspot. Check your support ticket creation pipelines.')

    except Exception as e:
        if settings.HUBSPOT_API_KEY is None:
            logger.warning(
                "Attempted to start the HubSpot client but no api key given. Generate an api key over at hubspot, "
                "then add it to the app as an environment variable (config var on heroku)."
            )
            return None, None, None

        if settings.DEBUG:
            logger.warning(
                "Error initialising connection to HubSpot CRM. Perhaps you have no internet connection? Error was %s",
                getattr(e, "message", "unknown"),
            )

        raise

    return support_pipeline, support_stage, subscription_statuses


support_pipeline, support_stage, subscription_statuses = initialise()


def get_or_create_contact(email):
    """ Get a contact from hubspot. If they don't exist, create them
    :param email: client's email address
    :return:
    """
    created = False
    try:
        contact = client.contacts.get_by_email(email)
    except HubspotNotFound:
        contact = client.contacts.create(data={"properties": [{"property": "email", "value": email}]})
        created = True

    return contact, created


def update_user_name(email, first_name, last_name):
    """ Use contact form submission to merge the name fields of a contact in hubspot.
    Check against name fields for registered octue users too.
    :param email:
    :param first_name:
    :param last_name:
    :return:
    """
    # TODO if a contact form is submitted, pick up the user name. Check for existence as an amy user
    pass


def subscribe_contact(email):
    """ Subscribe a contact to all of the email subscription types
    :param email:
    :return:
    """
    client.email_subscription.update_subscriptions(
        email,
        subscriptions=subscription_statuses,
        portalSubscriptionLegalBasis="LEGITIMATE_INTEREST_CLIENT",
        portal_legal_basis_explanation="Clicked subscribe on octue.com on {}".format(datetime.utcnow()),
    )


def create_ticket(message, subject, contact):
    """ Create a support ticket associated to a contact
    :param message:
    :param subject:
    :param contact:
    :return:
    """
    ticket = client.tickets.create(
        pipeline=support_pipeline, stage=support_stage, properties={"subject": subject, "content": message}
    )
    if contact is not None:
        client.crm_associations.create(
            from_object=ticket["objectId"],
            to_object=contact["vid"],
            definition=AssociationDefinitions.TICKET_TO_CONTACT,
        )
