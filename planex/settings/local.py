from .base import *  # noqa: F403


# DIRECTORIES AND ENVIRONMENT


# APP CONFIGURATION

DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG


# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="`c}ycP0(JRg*azi<<|=8d>?vH#@xI:P?Yksdc?Zog$~WZHw|oi")


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

# Serve compressed and cached static files
# TIP: Uncomment, then run npm install (root dir) and collectstatic to diagnose static files problems
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA FILES


# AUTH SETTINGS, PASSWORD STORAGE/VALIDATION, OAUTH2

AUTH_PASSWORD_VALIDATORS = []


# DJANGO UTILITIES


# REDIS and CELERY

# In development, all tasks will be executed locally by blocking until the task returns
CELERY_TASK_ALWAYS_EAGER = False


# WAGTAIL CONTENT MANAGEMENT SYSTEM

# URL for the preview iframe. Should point at Gatsby.
PREVIEW_URL = "http://localhost:8001/preview"


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


# INTEGRATIONS - AWS


# INTEGRATIONS - GOOGLE


# INTEGRATIONS - GITHUB


# INTEGRATIONS - PLOTLY
