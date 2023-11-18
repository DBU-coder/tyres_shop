from django.contrib import admin
from django.contrib.admin import TabularInline
from django import forms

from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import ProductImage, ProductStatistic, Category, ProductType, ProductSpecification, \
    ProductSpecificationValue, Product


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3


class ProductSpecificationInline(TranslationTabularInline):
    model = ProductSpecification
    extra = 2


class ProductSpecificationValueInline(TranslationTabularInline):
    model = ProductSpecificationValue
    extra = 1

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js',
            'admin/js/product_type_specifications.js',
        )

@admin.register(ProductType)
class ProductTypeAdmin(TabbedTranslationAdmin):
    inlines = (ProductSpecificationInline,)


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = ('product_type', 'sku', 'brand', 'name', 'price', 'status')
    list_display_links = ('sku', 'name')
    search_fields = ('sku', 'brand', 'name')
    list_editable = ('status', 'price')
    list_filter = ('brand', 'status')
    readonly_fields = ('stripe_product_price_id',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = (
        ProductSpecificationValueInline,
        ProductImageInline,
    )


@admin.register(ProductStatistic)
class ProductStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'purchases_quantity')
    search_fields = ('__str__',)


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name',)
    readonly_fields = ('slug',)
