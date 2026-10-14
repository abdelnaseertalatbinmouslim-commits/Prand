from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "عضو / طالب"),
        ("moderator", "مسؤول"),
        ("admin", "مدير المنصة"),
    ]
    username = models.CharField(max_length=150, unique=True, blank=True)
    phone = models.CharField("رقم الهاتف", max_length=20, unique=True)
    display_name = models.CharField("الاسم الظاهر", max_length=120, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    is_approved = models.BooleanField("مقبول من الإدارة", default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone
        if not self.display_name:
            self.display_name = self.get_full_name() or self.phone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} ({self.phone})"

class Course(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    category = models.CharField(max_length=100, default="أساسيات البرمجة")
    level = models.CharField(max_length=50, default="مبتدئ")
    cover = models.ImageField(upload_to="course_covers/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} — {self.title}"

class CodeSnippet(models.Model):
    title = models.CharField(max_length=180)
    language = models.CharField(max_length=50, default="python")
    description = models.TextField(blank=True)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Resource(models.Model):
    KIND_CHOICES = [
        ("tool", "أداة"),
        ("extension", "إضافة"),
        ("definition", "مصطلح وتعريف"),
        ("game", "لعبة تعليمية"),
        ("article", "مقال"),
    ]
    title = models.CharField(max_length=180)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="tool")
    description = models.TextField()
    url = models.URLField(blank=True)
    icon = models.CharField(max_length=40, default="✦")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
