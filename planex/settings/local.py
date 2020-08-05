from .base import *  # noqa: F403


# DIRECTORIES AND ENVIRONMENT


# APP CONFIGURATION

DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# Note: This key only used for development
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

# CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""}}


# INTERNATIONALISATION


# TEMPLATE CONFIGURATION


# STATIC FILES


# Serve compressed and cached static files
# TIP: Uncomment, then run npm install (root dir) and collectstatic to diagnose static files problems
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

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
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "app": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "cms_core": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "cms_site": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "crm": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django.db.backends": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "wagtail": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "django.request": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "django.security": {"level": "WARNING", "handlers": ["console"], "propagate": False},
    },
}


# INTEGRATIONS - GOOGLE

# GA_ID = env.str('GOOGLE_ANALYTICS_ID') Missing ID suppresses rendering of the GA code in non-production environments
GA_KEY_CONTENT = env.str("DEVELOPERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY")
GA_VIEW_ID = f'ga:{env.str("DEVELOPERS_GOOGLE_ANALYTICS_VIEW_ID")}'
