import os
import environ
from corsheaders.defaults import default_headers

import sys


# DIRECTORIES AND ENVIRONMENT

# Set the root directories
#
#   REPO_DIR (planex-cms/)               Top level working directory at runtime. Contains dependency files, builds, staticfiles, READMEs, etc
#   ROOT_DIR (planex-cms/planex/)        Root of the server code. Used by third party apps.
#   APPS_DIR (planex-cms/planex/core)    The django application configuration modules
#   SETTINGS_DIR (amy/backend/settings)  The django settings directory
REPO_DIR = environ.Path(__file__).__sub__(3)  # (planex-cms/planex/settings/base.py - 3 = planex-cms/)
ROOT_DIR = REPO_DIR.path("planex").__str__()
APP_DIR = REPO_DIR.path("planex").path("app").__str__()
SETTINGS_DIR = REPO_DIR.path("planex").path("settings").__str__()

# Add the backend directory to the system path so django can find the apps without renaming them to e.g. backend.pink
# (from https://stackoverflow.com/questions/3948356/how-to-keep-all-my-django-applications-in-specific-folder)
sys.path.insert(0, ROOT_DIR.__str__())


# Load operating system environment variables and then prepare to use them
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env file will only be used if not defined as environment variables
    env_file = str(REPO_DIR.path(".env"))
    print("Loading environment from file: {}\n".format(env_file))
    env.read_env(env_file)


# APP CONFIGURATION

ALLOWED_HOSTS = [
    "localhost",
    ".localhost",
    "0.0.0.0",
    "127.0.0.1",
    "octue.dev",
    ".octue.dev",
    "octue.com",
    ".octue.com",
]

DEBUG = env.bool("DJANGO_DEBUG", False)

INSTALLED_APPS = [
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtailmarkdown",
    "wagtail.contrib.postgres_search",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "raven.contrib.django.raven_compat",
    "captcha",
    "wagtailcaptcha",
    "wagtailfontawesome",
    "wagtailmenus",
    "phonenumber_field",
    "corsheaders",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_extensions",
    "fontawesome_5",
    "storages",
    "jsoneditor",
    "cms_core.apps.CMSCoreAppConfig",
    "cms_site.apps.CMSSiteAppConfig",
    "grapple",
    "graphene_django",
    "channels",
]


# MIDDLEWARE CONFIGURATION

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Must be placed above anything that can generate a response
    "corsheaders.middleware.CorsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


# CORS CONFIGURATION

CORS_URLS_REGEX = r"^(\/graphql\/.*)|(\/review\/api\/.*)$"
CORS_ORIGIN_WHITELIST = [
    "https://www.octue.com",
    "https://octue-production.netlify.com",
    "https://octue-staging.netlify.com",
]
CORS_ALLOW_HEADERS = default_headers + ("x-review-token",)


# EMAIL CONFIGURATION

DEFAULT_FROM_EMAIL = env.str("DJANGO_DEFAULT_FROM_EMAIL", default="The Octue Team <noreply@octue.com>")
EMAIL_SUBJECT_PREFIX = env.str("DJANGO_EMAIL_SUBJECT_PREFIX", default="")
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_BACKEND = env.str("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")


# MANAGER CONFIGURATION

# A list of all the people who get code error notifications.
# When DEBUG=False and a view raises an exception, Django will email these people with the full exception information.
# Each item in the list should be a tuple of (Full name, email address). Example:
ADMINS = [("Tom Clark", "tom@octue.com")]
MANAGERS = [("Tom Clark", "tom@octue.com")]
SUPPORT_TEAM = [
    ("Tom Clark", "tom@octue.com"),
]


# DATABASE CONFIGURATION

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://postgres_user:postgres_password@db/postgres_db"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# CACHING CONFIGURATION

# Front-end cache
# https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html

# TODO set up cloudflare
# if 'FRONTEND_CACHE_PURGE_URL' in env:
#     INSTALLED_APPS.append('wagtail.contrib.frontend_cache')
#     WAGTAILFRONTENDCACHE = {
#         'default': {
#             'BACKEND': 'wagtail.contrib.frontend_cache.backends.HTTPBackend',
#             'LOCATION': env['FRONTEND_CACHE_PURGE_URL'],
#         },
#     }
# elif 'FRONTEND_CACHE_CLOUDFLARE_TOKEN' in env:
#     INSTALLED_APPS.append('wagtail.contrib.frontend_cache')
#     WAGTAILFRONTENDCACHE = {
#         'default': {
#             'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
#             'EMAIL': env['FRONTEND_CACHE_CLOUDFLARE_EMAIL'],
#             'TOKEN': env['FRONTEND_CACHE_CLOUDFLARE_TOKEN'],
#             'ZONEID': env['FRONTEND_CACHE_CLOUDFLARE_ZONEID'],
#         },
#     }
#
# # Set s-max-age header that is used by reverse proxy/front end cache. See
# # urls.py
# try:
#     CACHE_CONTROL_S_MAXAGE = int(env.get('CACHE_CONTROL_S_MAXAGE', 600))
# except ValueError:
#     pass
#
#
# # Give front-end cache 30 second to revalidate the cache to avoid hitting the
# # backend. See urls.py
# CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
#     env.get('CACHE_CONTROL_STALE_WHILE_REVALIDATE', 30)
# )

# Do not use the same Redis instance for other things like Celery!
if "REDIS_URL" in env:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.url("REDIS_URL", default="redis://:redis_password@redis:6379"),
        }
    }
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.db.DatabaseCache", "LOCATION": "database_cache"}}


# INTERNATIONALISATION

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# Not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-gb"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# TEMPLATE CONFIGURATION

# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APP_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]


# STATIC FILES

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = str(os.path.join(str(REPO_DIR), "static_files"))
STATIC_URL = "/static/"

# Additional directories to search for static files
STATICFILES_DIRS = [
    str(os.path.join(APP_DIR, "static")),
]

# MEDIA FILES
MEDIA_ROOT = os.path.join(str(REPO_DIR), "media_files")
MEDIA_URL = "/media/"


# UPLOADED FILES

# Allow large body requests for figures to be uploaded. 100Mb, up from the default 2.5mb
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600


# WSGI/URL CONFIGURATION

ROOT_URLCONF = "planex.app.urls"
WSGI_APPLICATION = "planex.app.wsgi.application"


# AUTH SETTINGS, PASSWORD STORAGE AND VALIDATION

# Hashing algorithm
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# DJANGO UTILITIES

AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"


# REDIS and CELERY


# WAGTAIL CONTENT MANAGEMENT SYSTEM

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "https://www.octue.com"

# Grapple config
GRAPHENE = {"SCHEMA": "grapple.schema.schema"}
GRAPPLE_APPS = {"cms_core": "", "cms_site": ""}
GRAPPLE_ADD_SEARCH_HIT = True

# Previews
#  Wagtail previews are served from the frontend site, this URL is where they are directed to
if "PREVIEW_URL" in env:
    PREVIEW_URL = env.url("PREVIEW_URL")

# Search
WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.contrib.postgres_search.backend"},
}

WAGTAIL_SITE_NAME = "planex"
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILDOCS_DOCUMENT_MODEL = "cms_core.AccreditedDocument"  # Do not change this. Bad things will happen.
WAGTAILIMAGES_IMAGE_MODEL = "cms_core.AccreditedImage"  # Do not change this. Bad things will happen.


# BUILDS


# TESTING


# LOGGING


# INTEGRATIONS - GOOGLE

GOOGLE_ANALYTICS_ID = None
# Test keys as per https://developers.google.com/recaptcha/docs/faq
#   "With the following test keys, you will always get No CAPTCHA and all verification requests will pass."
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
NOCAPTCHA = True

SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# INTEGRATIONS - HUBSPOT
# If 'None' the
HUBSPOT_API_KEY = env.str("HUBSPOT_API_KEY", None)


# INTEGRATIONS - NETLIFY

NETLIFY_TRIGGER_URL = env.str("NETLIFY_TRIGGER_URL", "http://localhost:8000")
NETLIFY_AUTO_DEPLOY = env.str("NETLIFY_AUTO_DEPLOY", True)
