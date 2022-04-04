from django.contrib import admin
from .models import Category, Product,Attribute
# Register your models here.

class AttributeInline(admin.TabularInline):
    model = Attribute
    raw_id_fields = ['attribute']
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price','Inventory', 'created', 'updated']
    list_filter = ['category', 'created', 'updated']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    inlines = [AttributeInline]

admin.site.register(Product, ProductAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name","value","attribute")

admin.site.register(Attribute,AttributeAdmin)

