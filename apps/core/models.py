from django.db import models


class SiteProfile(models.Model):
    """Single-row site-wide settings editable from the admin."""
    name = models.CharField(max_length=100, default="Basanta Singh")
    tagline = models.CharField(max_length=200, default="Data Scientist · AI/ML Engineer · Educator")
    bio_short = models.TextField(help_text="2–3 sentence homepage bio")
    bio_long = models.TextField(help_text="Full about page bio (supports Markdown)")
    avatar = models.ImageField(upload_to="core/", blank=True)
    cv_file = models.FileField(upload_to="core/cv/", blank=True,
                               help_text="PDF CV for download")
    email = models.EmailField(default="mailbasantasingh@gmail.com")
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True, default="Biratnagar, Nepal")

    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    orcid_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    researchgate_url = models.URLField(blank=True)

    meta_description = models.TextField(max_length=160, blank=True)
    google_analytics_id = models.CharField(max_length=30, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Profile"
        verbose_name_plural = "Site Profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"bio_short": "", "bio_long": ""})
        return obj


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.name} — {self.subject[:50]}"
