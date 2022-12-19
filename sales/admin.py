from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date', 'get_html_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    # prepopulated_fields = {'slug': ('title',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Sale, SaleAdmin)
admin.site.register(Category, CategoryAdmin)
