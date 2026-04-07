"""
Base settings shared across all environments.
"""
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# ── Applications ────────────────────────────────────────────────
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = [
    "django_summernote",
    "taggit",
    "axes",
    "meta",
]

LOCAL_APPS = [
    "apps.core",
    "apps.blog",
    "apps.teaching",
    "apps.projects",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

# ── Middleware ───────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",                  # brute-force protection
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",                    # Content Security Policy
]

ROOT_URLCONF = "config.urls"

# ── Templates ────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── Database ─────────────────────────────────────────────────────
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}

# ── Password validation ──────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalisation ─────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# ── Static & Media ───────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Email ────────────────────────────────────────────────────────
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@basantasingh.com")
CONTACT_EMAIL = env("CONTACT_EMAIL", default="mailbasantasingh@gmail.com")

# ── Security: Axes (brute-force login protection) ────────────────
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1          # hours
AXES_LOCKOUT_CALLABLE = "apps.core.security.axes_lockout_response"
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_PARAMETERS = ["ip_address", "username"]

# ── Security: CSP ────────────────────────────────────────────────
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdnjs.cloudflare.com",
    "https://fonts.googleapis.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "https://fonts.googleapis.com",
    "https://cdnjs.cloudflare.com",
    "'unsafe-inline'",           # needed for summernote inline styles
)
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FRAME_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)

# ── Security: Rate limiting ──────────────────────────────────────
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"

# ── Cache ────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / ".cache",
    }
}

# ── Summernote (WYSIWYG editor) ──────────────────────────────────
SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": "400px",
        "toolbar": [
            ["style", ["bold", "italic", "underline", "clear"]],
            ["font", ["strikethrough", "superscript", "subscript"]],
            ["fontsize", ["fontsize"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["insert", ["link", "picture", "hr"]],
            ["view", ["fullscreen", "codeview"]],
        ],
    },
    "attachment_require_authentication": True,
    "attachment_filesize_limit": 5 * 1024 * 1024,  # 5 MB
}

# ── Taggit ───────────────────────────────────────────────────────
TAGGIT_CASE_INSENSITIVE = True

# ── Django-meta (SEO) ────────────────────────────────────────────
META_SITE_PROTOCOL = "https"
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_TWITTER_TYPE = "summary_large_image"
META_TWITTER_SITE = "@basantasingh"

# ── Site profile ─────────────────────────────────────────────────
SITE_NAME = "Basanta Singh"
SITE_TAGLINE = "Data Scientist · AI/ML Engineer · Educator"
SITE_DESCRIPTION = (
    "Portfolio and blog of Basanta Singh — Data Scientist, AI/ML Engineer, "
    "and Lecturer specialising in NLP, deep learning, and applied AI."
)
LINKEDIN_URL = "https://linkedin.com/in/basantasingh"
GITHUB_URL = "https://github.com/basantasingh"
GOOGLE_SCHOLAR_URL = ""
ORCID_URL = ""
