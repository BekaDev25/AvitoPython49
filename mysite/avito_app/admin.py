from django.contrib import admin
from.models import (Category, Products, UserProfile, SubCategory,
                    ProductImages, Review, Cart)
from modeltranslation.admin import TranslationAdmin

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(Category, SubCategory)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Products)
class ProductsAdmin(TranslationAdmin):
    inlines = [ProductImagesInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Cart)
