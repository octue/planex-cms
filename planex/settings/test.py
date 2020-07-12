from .base import *  # noqa: F403


# DIRECTORIES AND ENVIRONMENT


# APP CONFIGURATION

DEBUG = env.bool("DJANGO_DEBUG", default=False)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# Note: This key only used for test
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="6w1o8j5+a%i856735=i&gdrlgiqf25jjt9u8zazj5eymqq9%++")


# MIDDLEWARE CONFIGURATION


# SECURITY CONFIGURATION
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SECURE_SSL_REDIRECT = False
CORS_ORIGIN_ALLOW_ALL = True


# EMAIL CONFIGURATION

EMAIL_PORT = 1025
EMAIL_HOST = "localhost"
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")


# MANAGER CONFIGURATION


# DATABASE CONFIGURATION


# CACHING CONFIGURATION

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}


# INTERNATIONALISATION


# TEMPLATE CONFIGURATION


# STATIC FILES

# TODO use GCP and hook in for proper test
# Serve compressed and cached static files
# TIP: Uncomment, then run npm install (root dir) and collectstatic to diagnose static files problems
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA FILES


# AUTH SETTINGS, PASSWORD STORAGE/VALIDATION, OAUTH2

AUTH_PASSWORD_VALIDATORS = []


# DJANGO UTILITIES


# REDIS and CELERY


# WAGTAIL CONTENT MANAGEMENT SYSTEM


# API


# TESTING
TEST_RUNNER = "django.test.runner.DiscoverRunner"
TESTING = env.bool("TESTING", default=True)


# LOGGING

# Console only, debug level for local development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {
        "verbose": {"format": "%(levelname)s \t%(asctime)s %(module)s \t" "%(process)d %(thread)d \t%(message)s"}
    },
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "wagtail": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}


# INTEGRATIONS - GOOGLE

# GA_ID = env.str('GOOGLE_ANALYTICS_ID') Missing ID suppresses rendering of the GA code in non-production environments
GA_KEY_FILEPATH = str(os.path.join(REPO_DIR, ".travis-gcp-test-account.json"))
GA_VIEW_ID = f'ga:{env.str("TEST_GOOGLE_ANALYTICS_VIEW_ID")}'
