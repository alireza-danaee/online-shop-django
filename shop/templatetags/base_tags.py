from django import template

from shop.models import Category 

from django.contrib.contenttypes.models import ContentType




register = template.Library()






@register.inclusion_tag('product/partials/category_navbar.html')
def category_navbar():
    return {
        'category': Category.objects.all(),
        
    }



























