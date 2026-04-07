from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category


def post_list(request):
    queryset = Post.published.select_related("author", "category").prefetch_related("tags")
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    query = request.GET.get("q", "").strip()

    active_category = None
    active_tag = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        queryset = queryset.filter(category=active_category)

    if tag_slug:
        queryset = queryset.filter(tags__slug=tag_slug)
        active_tag = tag_slug

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(body__icontains=query)
        )

    paginator = Paginator(queryset, 9)
    page = paginator.get_page(request.GET.get("page"))
    categories = Category.objects.all()

    return render(request, "blog/list.html", {
        "page_obj": page,
        "categories": categories,
        "active_category": active_category,
        "active_tag": active_tag,
        "query": query,
    })


def post_detail(request, year, month, slug):
    post = get_object_or_404(
        Post.published.select_related("author", "category").prefetch_related("tags"),
        published_at__year=year,
        published_at__month=month,
        slug=slug,
    )
    related = Post.published.filter(
        category=post.category
    ).exclude(pk=post.pk).order_by("-published_at")[:3]

    return render(request, "blog/detail.html", {
        "post": post,
        "related_posts": related,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related("author")
    paginator = Paginator(posts, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": page,
    })
