from django.conf import settings
from .models import SiteProfile


def site_settings(request):
    profile = SiteProfile.get()
    return {
        "site_name": getattr(settings, "SITE_NAME", "Basanta Singh"),
        "site_tagline": getattr(settings, "SITE_TAGLINE", ""),
        "linkedin_url": profile.linkedin_url or getattr(settings, "LINKEDIN_URL", ""),
        "github_url": profile.github_url or getattr(settings, "GITHUB_URL", ""),
        "google_scholar_url": profile.google_scholar_url,
        "orcid_url": profile.orcid_url,
        "twitter_url": profile.twitter_url,
        "profile": profile,
    }
