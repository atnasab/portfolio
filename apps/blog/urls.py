from django.urls import path
from django.contrib.syndication.views import Feed
from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("feed/", LatestPostsFeed(), name="feed"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("<int:year>/<str:month>/<slug:slug>/", views.post_detail, name="detail"),
]
