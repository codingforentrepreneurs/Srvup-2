from django.contrib import admin

# Register your models here.

from .forms import CategoryAdminForm
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title']
    form = CategoryAdminForm
    # class Meta:
    #     model = Category

    def short_title(self, obj):
        return obj.title[:3]

admin.site.register(Category, CategoryAdmin)
