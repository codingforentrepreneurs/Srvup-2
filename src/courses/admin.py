from django.contrib import admin

# Register your models here.

from .models import Course, Lecture

class LectureInline(admin.TabularInline):
    model = Lecture

class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'description']

    class Meta:
        model = Course

    def short_title(self, obj):
        return obj.title[:3]

admin.site.register(Course, CourseAdmin)

