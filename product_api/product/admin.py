from django.contrib import admin

from .models import Category, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    search_fields = ('name', 'slug', 'image')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    search_fields = ('name', 'slug', 'image')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
