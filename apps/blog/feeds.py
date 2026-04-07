from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Basanta Singh — Blog"
    description = "Latest articles on AI, ML, NLP and data science."

    def link(self):
        return reverse("blog:list")

    def items(self):
        return Post.published.order_by("-published_at")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_pubdate(self, item):
        return item.published_at
