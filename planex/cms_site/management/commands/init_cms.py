from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from wagtail.core.models import Page, Site
from cms_site.models import SitePage
import logging


logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """ Use `python manage.py help init_site` to display help for this command line administration tool
    """

    help = "Initialises application from a newly reset and migrated database with only wagtail's default site and root page"

    def add_arguments(self, parser):
        """
        :return void
        """
        parser.add_argument(
            "--user", "-u", nargs=1, required=True, dest="user", default=None, help="Specify the email address of the user who will own the generated pages",
        )

    def handle(self, *args, **options):
        """ Runs manage.py init_site to add base data
        :return void
        """
        # Get the user instance
        user_email = options["user"][0]
        try:
            admin_user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise CommandError('user "{}" does not exist'.format(user_email))

        # Wagtail forces creation of a default root page which is uneditable in Wagtail CMS so you have to have it
        # but it's completely useless and not owned by you.
        # Also, the inability to edit the root means that even if you have a single site, your site root page
        # can never be your root page. Your site root page (aka 'home') has a slug so to get the url path you have to do
        # some surgery to remove the first part of the path. It's nothing but a huge PAIN IN THE ASSHOLE.
        # The offensive code is here:
        # https://github.com/wagtail/wagtail/blob/8c306910dd86e09cea11196715da47c6a54c722b/wagtail/core/migrations/0002_initial_data.py#L19
        default_root_page = Page.objects.first()
        path = default_root_page.path
        depth = default_root_page.depth
        default_root_page.delete()

        # Make a new Root Page
        root_page = Page(title="Octue Root", slug="root", path=path, depth=depth, owner=admin_user)
        root_page.save()
        revision = root_page.save_revision()
        revision.publish()

        # Make a new Home Page
        home_page = SitePage(title="Octue Home", slug="home", show_in_menus=True, owner=admin_user)
        root_page.add_child(instance=home_page)
        revision = home_page.save_revision()
        revision.publish()

        # Create other (non-root) pages as children of the home page
        pages = [
            SitePage(title="About", slug="about", show_in_menus=True, owner=admin_user),
            # BlogPage(title='Blog', slug='blog', show_in_menus=True, owner=admin_user),
            SitePage(title="Contact", slug="contact", show_in_menus=True, owner=admin_user),
            # BlogPage(title="Press and announcements", slug='press', show_in_menus=True, owner=admin_user),
            SitePage(title="Terms and conditions", slug="terms", show_in_menus=True, owner=admin_user),
        ]

        # Add as children to the root (Home) page, and publish
        for page in pages:
            try:
                home_page.add_child(instance=page)
                revision = page.save_revision()
                revision.publish()
            except Exception as e:
                # Do not fail to deploy the app, but warn instead (will show in the heroku buildlog)
                logger.error(e)
                logger.warning("Skipping creation of `/%s/` page... check it's correctly created already", page.slug)

        # Create or update the default site. NB can't use django's update_or_create as we need to fetch the first() item
        site = Site.objects.first()
        if site:
            site.hostname = "www.octue.com"
            site.site_name = "Octue"
            site.root_page = home_page
            site.is_default_site = True
        else:
            site = Site.objects.create(hostname="www.octue.com", site_name="Octue", root_page=home_page, is_default_site=True)

        site.save()
