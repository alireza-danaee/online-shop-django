from django.contrib import admin
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'created', 'updated']
    list_filter = ['category', 'created', 'updated']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
