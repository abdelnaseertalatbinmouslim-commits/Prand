from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Lesson, CodeSnippet, Resource

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("phone", "display_name", "role", "is_approved", "is_staff")
    list_filter = ("role", "is_approved", "is_staff")
    search_fields = ("phone", "display_name")
    fieldsets = UserAdmin.fieldsets + (
        ("بيانات المنصة", {"fields": ("phone", "display_name", "role", "is_approved")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("بيانات المنصة", {"fields": ("phone", "display_name", "role", "is_approved")}),
    )

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "is_published")
    list_filter = ("category", "level", "is_published")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "created_at")
    search_fields = ("title", "language", "description")

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "is_featured")
    list_filter = ("kind", "is_featured")
    search_fields = ("title", "description")
