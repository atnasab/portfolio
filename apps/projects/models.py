from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Project(models.Model):
    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField(help_text="Full description (Markdown supported)")
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.COMPLETED)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    # Tech stack
    technologies = models.CharField(max_length=300, blank=True,
                                    help_text="Comma-separated: Python, PyTorch, …")
    tags = TaggableManager(blank=True)

    # Links
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    paper_url = models.URLField(blank=True)
    blog_post = models.ForeignKey(
        "blog.Post", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="projects",
        help_text="Link to a related blog post"
    )

    # Metrics (optional display badges)
    metric_label = models.CharField(max_length=60, blank=True, help_text="e.g. Accuracy")
    metric_value = models.CharField(max_length=30, blank=True, help_text="e.g. 97.3%")

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]
