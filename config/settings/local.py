from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS += ["debug_toolbar"]  # noqa

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa

INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SUMMERNOTE_CONFIG = {
    **SUMMERNOTE_CONFIG,  # noqa
    "iframe": False,
}
