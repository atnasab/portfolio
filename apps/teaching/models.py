from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Subject(models.Model):
    """A subject/module currently or previously taught."""

    LEVEL_CHOICES = [
        ("undergraduate", "Undergraduate"),
        ("postgraduate", "Postgraduate"),
        ("professional", "Professional Development"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    code = models.CharField(max_length=20, blank=True, help_text="e.g. CS301")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="undergraduate")
    institution = models.CharField(max_length=200)
    partner_university = models.CharField(max_length=200, blank=True,
                                          help_text="e.g. University of Wolverhampton, UK")
    description = models.TextField()
    syllabus = models.TextField(blank=True, help_text="Markdown list of topics covered")
    cover_image = models.ImageField(upload_to="teaching/covers/", blank=True)
    icon_class = models.CharField(max_length=60, blank=True,
                                  help_text="Font Awesome class e.g. fa-brain")

    # Delivery info
    academic_year = models.CharField(max_length=20, blank=True, help_text="e.g. 2024–25")
    semester = models.CharField(max_length=40, blank=True)
    credits = models.PositiveSmallIntegerField(null=True, blank=True)
    students_count = models.PositiveSmallIntegerField(null=True, blank=True)

    # Links
    course_url = models.URLField(blank=True, help_text="External course/module page")
    materials_url = models.URLField(blank=True, help_text="Slides / GitHub / Drive link")
    syllabus_pdf = models.FileField(upload_to="teaching/syllabi/", blank=True)

    is_active = models.BooleanField(default=True, help_text="Currently teaching?")
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-academic_year", "title"]

    def __str__(self):
        return f"{self.title} — {self.institution}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.institution}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teaching:detail", kwargs={"slug": self.slug})

    @property
    def syllabus_topics(self):
        """Return list of topic strings parsed from Markdown bullet list."""
        topics = []
        for line in self.syllabus.splitlines():
            line = line.strip().lstrip("-*•").strip()
            if line:
                topics.append(line)
        return topics
