from django.contrib import admin

from .models import Category, SubCategory, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'image')
    search_fields = (
        'name', 'slug', 'image')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'image')
    search_fields = (
        'name', 'slug', 'image')


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'image_original', 'price', 'subcategory', 'category')
    search_fields = (
        'name', 'slug', 'image_original', 'price', 'subcategory', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
