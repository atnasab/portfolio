from django.http import HttpResponse


def axes_lockout_response(request, credentials=None, *args, **kwargs):
    """Custom response when Axes locks out an IP/username."""
    return HttpResponse(
        "Too many failed login attempts. Please try again in 1 hour.",
        status=429,
        content_type="text/plain",
    )
