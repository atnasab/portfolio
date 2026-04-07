from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
import markdown
import bleach

User = get_user_model()

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li", "h2", "h3", "h4",
    "blockquote", "code", "pre", "a", "img", "table", "thead", "tbody",
    "tr", "th", "td", "hr",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "*": ["class"],
}


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#2E86AB",
                             help_text="Hex color for the category badge")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="published_at", blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="posts")
    cover_image = models.ImageField(upload_to="blog/covers/%Y/%m/", blank=True)
    cover_alt = models.CharField(max_length=200, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Short summary (max 300 chars)")
    body = models.TextField(help_text="Markdown or HTML via Summernote")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    canonical_url = models.URLField(blank=True)

    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["status", "-published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={
            "year": self.published_at.year,
            "month": self.published_at.strftime("%m"),
            "slug": self.slug,
        })

    @property
    def body_html(self):
        """Render body as sanitized HTML (supports Markdown)."""
        raw_html = markdown.markdown(
            self.body,
            extensions=["fenced_code", "tables", "toc", "nl2br"],
        )
        return bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)

    @property
    def reading_time(self):
        word_count = len(self.body.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    @property
    def effective_meta_title(self):
        return self.meta_title or self.title

    @property
    def effective_meta_description(self):
        return self.meta_description or self.excerpt
