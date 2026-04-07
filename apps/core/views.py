import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseServerError
from django_ratelimit.decorators import ratelimit

from .models import SiteProfile, ContactMessage
from .forms import ContactForm
from apps.blog.models import Post
from apps.projects.models import Project
from apps.teaching.models import Subject

logger = logging.getLogger(__name__)


def home(request):
    profile = SiteProfile.get()
    recent_posts = Post.published.order_by("-published_at")[:3]
    featured_projects = Project.objects.filter(is_featured=True).order_by("order")[:4]
    subjects = Subject.objects.filter(is_active=True).order_by("order")[:6]
    return render(request, "core/home.html", {
        "profile": profile,
        "recent_posts": recent_posts,
        "featured_projects": featured_projects,
        "subjects": subjects,
    })


def about(request):
    profile = SiteProfile.get()
    return render(request, "core/about.html", {"profile": profile})


@ratelimit(key="ip", rate="5/h", method="POST", block=True)
def contact(request):
    profile = SiteProfile.get()
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        ip = _get_client_ip(request)
        msg = ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
            ip_address=ip,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        try:
            send_mail(
                subject=f"[Portfolio Contact] {msg.subject}",
                message=(
                    f"From: {msg.name} <{msg.email}>\n\n{msg.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Failed to send contact email for message id=%s", msg.pk)

        messages.success(request, "Thanks! Your message has been sent.")
        return redirect("core:contact")

    return render(request, "core/contact.html", {"form": form, "profile": profile})


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)


def _get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
