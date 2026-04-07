"""
Production settings for DigitalOcean deployment.
"""
from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# ── Security headers (production only) ──────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ── Database (PostgreSQL via env) ────────────────────────────────
DATABASES = {
    "default": env.db("DATABASE_URL")  # noqa
}
DATABASES["default"]["CONN_MAX_AGE"] = 60

# ── Cache (file-based for basic DO plan, upgrade to Redis later) ─
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/cache/portfolio",
    }
}

# ── Logging ──────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/portfolio/django.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# ── Sentry error tracking ────────────────────────────────────────
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# ── Email (SMTP) ─────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ── Admin URL obfuscation ────────────────────────────────────────
ADMIN_URL = env("ADMIN_URL", default="secure-admin/")
