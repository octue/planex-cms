from .base import *  # noqa: F403


# DIRECTORIES AND ENVIRONMENT


# APP CONFIGURATION

# Always set to false in production
DEBUG = False

# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")


INSTALLED_APPS += [
    "gunicorn",
]
INSTALLED_APPS += [
    "anymail",
]
INSTALLED_APPS += [
    "storages",
]


# MIDDLEWARE CONFIGURATION

MIDDLEWARE += [
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
]


# SECURITY CONFIGURATION
# This ensures that Django will use only https requests and be able to detect a secure connection properly on Heroku
# See:
#   https://help.heroku.com/J2R1S4T8/can-heroku-force-an-application-to-use-ssl-tls
#   https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
#   https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
CSRF_TRUSTED_ORIGINS = [".octue.com"]
X_FRAME_OPTIONS = "DENY"


# EMAIL CONFIGURATION

ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_ACCESS_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SERVER_NAME", default="mg.octue.com"),
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"


# MANAGER CONFIGURATION


# DATABASE CONFIGURATION

# Unlike base, this raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES["default"] = env.db("DATABASE_URL")


# CACHING CONFIGURATION

# Use redis for caching in production (requires the location, not just the url)
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_LOCATION,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
#                                         # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         }
#     }
# }

# INTERNATIONALISATION


# TEMPLATE CONFIGURATION


# STATIC FILES

# Serve compressed and cached static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# MEDIA FILES

# Uploaded Media Files See: http://django-storages.readthedocs.io/en/latest/index.html
# TODO alternative user configuration for management of analyses/data storage, and conf. for user media files
AWS_ACCESS_KEY_ID = BOTO3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = BOTO3_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = "octue-amy-assets"
AWS_S3_REGION_NAME = "eu-west-1"
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7
# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
control = "max-age=%d, s-maxage=%d, must-revalidate" % (AWS_EXPIRY, AWS_EXPIRY)
AWS_HEADERS = {"Cache-Control": bytes(control, encoding="latin-1")}
# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
MEDIA_URL = "https://s3.amazonaws.com/{bucket}/".format(bucket=AWS_STORAGE_BUCKET_NAME)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# AUTH SETTINGS, PASSWORD STORAGE/VALIDATION, OAUTH2

# Set the URL to redirect users to in registration confirmation
AUTH_REGISTER_URL = "https://octue.com/register/"  # Appended with the signature created to verify the user

# DJANGO UTILITIES


# ELASTICSEARCH
ES_URL = os.environ.get("BONSAI_URL")

ELASTICSEARCH_DSL = {
    "default": {"hosts": ES_URL},
}

# Name of the Elasticsearch indices
ELASTICSEARCH_INDEX_NAMES = {
    "search.documents.applications": "prod_entities",
    "search.documents.twins": "prod_entities",
    "search.documents.users": "prod_entities",
}


# REDIS and CELERY


# CONTENT MANAGEMENT SYSTEM


# API
REDOC_LOGO_URL = "https://www.octue.com/static/images/assets_octue-api-logo.png"

# TESTING

# Always turn testing off in production
TESTING = False
TESTING_EXPENSIVE = False


# LOGGING

CORALOGIX_API_KEY = env("CORALOGIX_API_KEY")
CORALOGIX_APPLICATION_NAME = env("CORALOGIX_APPLICATION_NAME")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "ERROR", "handlers": ["console", "coralogix"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {
        "coralogix": {
            "class": "coralogix.handlers.CoralogixLogger",
            "level": "DEBUG",
            "formatter": "verbose",
            "private_key": CORALOGIX_API_KEY,
            "app_name": CORALOGIX_APPLICATION_NAME,
            "subsystem": "planex",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "app": {"level": "DEBUG", "handlers": ["console", "coralogix"], "propagate": False},
        "api": {"level": "INFO", "handlers": ["console", "coralogix"], "propagate": False},
        "cms": {"level": "DEBUG", "handlers": ["console", "coralogix"], "propagate": False},
        "datefinder": {"level": "INFO", "handlers": ["console", "coralogix"], "propagate": False},
        "momcorp": {"level": "INFO", "handlers": ["console", "coralogix"], "propagate": False},
        "nibbler": {"level": "INFO", "handlers": ["console", "coralogix"], "propagate": False},
        "pink": {"level": "INFO", "handlers": ["console", "coralogix"], "propagate": False},
        "search": {"level": "DEBUG", "handlers": ["console", "coralogix"], "propagate": False},
        "utils": {"level": "DEBUG", "handlers": ["console", "coralogix"], "propagate": False},
        "django.db.backends": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "WARNING",
            "handlers": ["console", "coralogix"],
            "propagate": False,
        },
    },
}


# INTEGRATIONS - AWS


# INTEGRATIONS - GOOGLE

# We want GA code to be rendered in production, but not in testing
GOOGLE_ANALYTICS_ID = "UA-43965341-2"

# Unlike base, this raises ImproperlyConfigured exception if RECAPTCHA_PRIVATE_KEY not in os.environ
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")


# INTEGRATIONS - GITHUB

# INTEGRATIONS - PLOTLY
