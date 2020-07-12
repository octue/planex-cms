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
BOTO3_ACCOUNT_ID = env.str("BOTO3_ACCOUNT_ID")
BOTO3_REGION = "eu-west-1"
BOTO3_SERVICES = ["s3"]
BOTO3_OPTIONAL_PARAMS = {"s3": {"config": {"addressing_style": "path"}}}
BOTO3_ACCESS_KEY = env.str("BOTO3_ACCESS_KEY")
BOTO3_SECRET_KEY = env.str("BOTO3_SECRET_KEY")

AWS_ACCESS_KEY_ID = BOTO3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = BOTO3_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = env.str("ASSETS_BUCKET_NAME")
AWS_S3_REGION_NAME = BOTO3_REGION
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


# DJANGO UTILITIES


# REDIS and CELERY


# TESTING

# Always turn testing off in production
TESTING = False


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
            "level": "INFO",
            "formatter": "verbose",
            "private_key": CORALOGIX_API_KEY,
            "app_name": CORALOGIX_APPLICATION_NAME,
            "subsystem": "planex",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "app": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "cms_core": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "cms_site": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "crm": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "django.db.backends": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "wagtail": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "django.request": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
        "django.security": {"level": "WARNING", "handlers": ["console", "coralogix"], "propagate": False},
    },
}


# INTEGRATIONS - GOOGLE

RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")

GA_ID = env.str("GOOGLE_ANALYTICS_ID")  # Causes the GA code to get rendered (in production pages)
GA_KEY_CONTENT = env.str("GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY")
GA_VIEW_ID = f'ga:{env.str("GOOGLE_ANALYTICS_VIEW_ID")}'
