from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import BlogSitemap
from apps.core.sitemaps import StaticSitemap

ADMIN_URL = getattr(settings, "ADMIN_URL", "admin/")

sitemaps = {
    "static": StaticSitemap,
    "blog": BlogSitemap,
}

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("summernote/", include("django_summernote.urls")),

    # Apps
    path("", include("apps.core.urls", namespace="core")),
    path("blog/", include("apps.blog.urls", namespace="blog")),
    path("teaching/", include("apps.teaching.urls", namespace="teaching")),
    path("projects/", include("apps.projects.urls", namespace="projects")),

    # SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler403 = "apps.core.views.error_403"
handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"
