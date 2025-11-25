from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug', 'description', 'category__name']

    readonly_fields = ['image_preview', 'created', 'updated']

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'price', 'stock', 'available')
        }),
        ('Media', {
            'fields': ('image', 'image_url', 'image_preview')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created', 'updated')
        }),
    )

    def _image_source(self, obj):
        if getattr(obj, 'image', None) and getattr(obj.image, 'url', None):
            return obj.image.url
        if getattr(obj, 'image_url', None):
            return obj.image_url
        return ''

    def thumbnail(self, obj):
        src = self._image_source(obj)
        if not src:
            return '-'
        return format_html('<img src="{}" style="height:60px; width:auto; object-fit:contain; border:1px solid #eee; padding:2px; background:#fff;"/>', src)

    thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        if not obj:
            return '-'
        src = self._image_source(obj)
        if not src:
            return '-'
        return format_html('<img src="{}" style="max-height:300px; width:auto; object-fit:contain; border:1px solid #eee; padding:4px; background:#fff;"/>', src)

    image_preview.short_description = 'Image preview'