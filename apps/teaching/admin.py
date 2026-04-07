from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "institution", "level", "academic_year", "is_active", "order")
    list_filter = ("level", "is_active", "institution")
    search_fields = ("title", "code", "institution")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("order", "is_active")
    fieldsets = (
        ("Course Info", {"fields": ("title", "slug", "code", "level", "institution",
                                    "partner_university", "description", "syllabus",
                                    "cover_image", "icon_class")}),
        ("Delivery", {"fields": ("academic_year", "semester", "credits", "students_count")}),
        ("Links & Files", {"fields": ("course_url", "materials_url", "syllabus_pdf")}),
        ("Display", {"fields": ("is_active", "order")}),
    )
