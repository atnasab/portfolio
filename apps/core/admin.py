from django.contrib import admin
from .models import SiteProfile, ContactMessage


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name", "tagline", "avatar", "bio_short", "bio_long", "cv_file")}),
        ("Contact", {"fields": ("email", "phone", "location")}),
        ("Social Links", {"fields": ("linkedin_url", "github_url", "google_scholar_url",
                                     "orcid_url", "twitter_url", "researchgate_url")}),
        ("SEO & Analytics", {"fields": ("meta_description", "google_analytics_id")}),
    )

    def has_add_permission(self, request):
        # Only allow adding if no profile exists yet
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent accidental deletion

    def changelist_view(self, request, extra_context=None):
        # Redirect list view directly to the single object
        profile = SiteProfile.get()
        from django.shortcuts import redirect
        return redirect(f"/admin/core/siteprofile/{profile.pk}/change/")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "ip_address",
                       "user_agent", "created_at")
    actions = ["mark_read"]

    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = "Mark selected messages as read"
