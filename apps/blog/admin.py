from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("body",)
    list_display = ("title", "author", "category", "status", "is_featured", "published_at")
    list_filter = ("status", "category", "is_featured")
    search_fields = ("title", "body", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    raw_id_fields = ("author",)
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "author", "category",
                                "cover_image", "cover_alt", "excerpt", "body")}),
        ("Publishing", {"fields": ("status", "is_featured", "published_at", "tags")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "canonical_url"),
                 "classes": ("collapse",)}),
    )
