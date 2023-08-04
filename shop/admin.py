from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import *


# For upload multiple images
class GalleryInline(GenericTabularInline):
    model = Gallery
    extra = 5


@admin.register(Tyre)
class TyreAdmin(admin.ModelAdmin):
    list_display = ('sku', 'brand', 'name', 'diameter', 'profile', 'season', 'vehicle_type', 'spikes', 'price', 'stock_qty', 'status')
    list_display_links = ('sku', 'name')
    search_fields = ('sku', 'brand', 'name')
    list_editable = ('status', 'price', 'stock_qty')
    list_filter = ('brand', 'season', 'diameter', 'vehicle_type', 'status')
    prepopulated_fields = {'slug': ('brand', 'width', 'profile', 'diameter', 'load_index', 'speed_index')}
    inlines = [GalleryInline]


@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('sku', 'brand', 'model', 'name', 'diameter', 'width', 'type', 'price', 'color', 'stock_qty', 'status')
    list_display_links = ('sku', 'model', 'name')
    search_fields = ('sku', 'brand', 'name')
    list_editable = ('status', 'price', 'stock_qty')
    list_filter = ('brand', 'diameter', 'width', 'type', 'status')
    prepopulated_fields = {'slug': ('brand', 'model', 'diameter', 'width', 'pcd', 'et', 'dia', 'color')}
    inlines = [GalleryInline]


admin.site.register(Category)
