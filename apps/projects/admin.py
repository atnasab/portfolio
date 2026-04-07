from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "is_featured", "order", "start_date", "end_date")
    list_filter = ("status", "is_featured")
    search_fields = ("title", "short_description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("order", "is_featured")
    fieldsets = (
        ("Project Info", {"fields": ("title", "slug", "short_description", "description",
                                     "cover_image", "status", "is_featured", "order")}),
        ("Tech & Tags", {"fields": ("technologies", "tags")}),
        ("Links", {"fields": ("github_url", "demo_url", "paper_url", "blog_post")}),
        ("Metrics", {"fields": ("metric_label", "metric_value")}),
        ("Dates", {"fields": ("start_date", "end_date")}),
    )
