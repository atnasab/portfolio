from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["core:home", "core:about", "core:contact",
                "blog:list", "teaching:list", "projects:list"]

    def location(self, item):
        return reverse(item)
